/*
* ****************************************************************************
*
* intset.c
*
* COMP9315 -- Assignment 1 
* Moyao Wang (z5099162), Shan Wang (z5119666) （Group name WW)
* Adding a Set Data Type to PostgreSQL
* 1st Sept. 2018
* 
* ****************************************************************************
*/
 
#include "postgres.h"
#include "fmgr.h"
#include "libpq/pqformat.h"     // needed for send/recv functions
#include "utils/builtins.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>


PG_MODULE_MAGIC;


// Functions assist self-defined operators
void isValid_changeFormat(char *src, char *dest);
void remove_duplicates(char *src, char *dest);
bool isSubsetOf(char *set1, char *set2);
bool contains(int val, char* str);
void union_sets(char *set1, char *set2, char *dest);
void intersection(char *set1, char *set2, char *dest);
void difference(char *set1, char *set2, char *dest);


// Self-defined operators
Datum intset_in(PG_FUNCTION_ARGS);
Datum intset_out(PG_FUNCTION_ARGS);
Datum intset_recv(PG_FUNCTION_ARGS);
Datum intset_send(PG_FUNCTION_ARGS);
Datum intset_contains(PG_FUNCTION_ARGS);
Datum intset_cardinality(PG_FUNCTION_ARGS);
Datum intset_subset(PG_FUNCTION_ARGS);
Datum intset_equal(PG_FUNCTION_ARGS);
Datum intset_union(PG_FUNCTION_ARGS);
Datum intset_intersection(PG_FUNCTION_ARGS);
Datum intset_difference(PG_FUNCTION_ARGS);
Datum intset_disjunction(PG_FUNCTION_ARGS);

 
// 1 - Check input, 2 - remove spaces
void isValid_changeFormat(char *src, char *dest)
{
    // Flags for checking if meets these chars in each session separated by comma
    // digit -- reached 0-9, number -- reached 1-9
    bool openCurly = false, closeCurly = false, digit = false, space = false, number = false, comma = false, minus = false;
    // i -- go through original string, 
    // index -- write to a new string in a consistent format
    int i, index;

    for (i = 0, index = 0; i < strlen(src); i++) {
        if (src[i] >= '0' && src[i] <= '9') { // 0-9
            if ((!openCurly) || closeCurly)// No open curly or reached close curly
                ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION), 
                    errmsg("Invalid input syntax for intset: \"%s\"", src)));
            else if (space && digit) // Space btwn digits
                ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION), 
                    errmsg("Invalid input syntax for intset: \"%s\"", src)));
            else if (src[i] >= '1' && src[i] <= '9') { // 1-9
                dest[index++] = src[i];
                number = true;
            } else if (src[i] == '0') {
                if (!number) {
                    if (src[i+1] < '0' || src[i+1] > '9') {// Check if is e.g. 00000
                        if (minus) // -0 is 0
                            dest[index-1] = '0';
                        else 
                            dest[index++] = src[i];
                    } else
                        continue; // 00001 is valid, remove 0s
                } else
                    dest[index++] = src[i]; // e.g. 10000000
            }

            comma = false;
            digit = true;
            space = false;

        } else if (src[i] == '{') { // Check open curly
            if (openCurly) // Check if open curly already exist
                ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION), 
                    errmsg("Invalid input syntax for intset: \"%s\"", src)));
            else if (index) // Check if there is any char before open curly
                ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION), 
                    errmsg("Invalid input syntax for intset: \"%s\"", src)));
            else {
                dest[index++] = src[i];
                openCurly = true;
            }

            comma = false;
            digit = false;
            space = false;

        } else if (src[i] == '}') { // Check close curly
            if (closeCurly) // Check if close curly already exist
                ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION), 
                    errmsg("Invalid input syntax for intset: \"%s\"", src)));
            else if (comma) // Check if there is any digit after last comma
                ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION), 
                    errmsg("Invalid input syntax for intset: \"%s\"", src)));
            else {
                dest[index++] = src[i];
                closeCurly = true;
            }

            comma = false;
            digit = false;
            space = false;
            minus = false;

        } else if (src[i] == ',') { // Check comma
            if ((!openCurly) || closeCurly) // No open curly or reached close curly
                ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION), 
                    errmsg("Invalid input syntax for intset: \"%s\"", src)));
            else if (comma) // 2 adjacent comma
                ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION), 
                    errmsg("Invalid input syntax for intset: \"%s\"", src)));
            else if (!digit) // No digit before comma
                ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION), 
                    errmsg("Invalid input syntax for intset: \"%s\"", src)));
            else
                dest[index++] = src[i];

            comma = true;
            digit = false;
            number = false;
            space = false;
            minus = false;

        } else if (src[i] == '-') { // Less than zero
            if ((!openCurly) || closeCurly) // No open curly or reached close curly
                ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION), 
                    errmsg("Invalid input syntax for intset: \"%s\"", src)));
            else if ((src[i-1] == ',' || src[i-1] == ' ' || src[i-1] == '{') && src[i+1] >= '0' && src[i+1] <= '9')
                dest[index++] = src[i];
            else if (digit) // No digit can before '-'
                ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION), 
                    errmsg("Invalid input syntax for intset: \"%s\"", src)));
            else
                ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION), 
                    errmsg("Invalid input syntax for intset: \"%s\"", src)));
            minus = true;

        } else if (src[i] == ' ') // Reach a space
            space = true;
        else // Other chars are invalid
            ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION), 
                errmsg("Invalid input syntax for intset: \"%s\"", src)));
    }

    if ((!openCurly) || (!closeCurly)) // Check if curly brace exist
        ereport(ERROR, (errcode (ERRCODE_INVALID_TEXT_REPRESENTATION),
            errmsg("Invalid input syntax for intset: \"%s\"", src)));

    dest[index] = '\0';
}


/* 
 * After checking validity and changing to a consistent format
 * Remove duplicate values e.g. {1,1,3,1,3,1} -> {,1,3,} 
 * (then remove the first and the last comma in another function)
 */
void remove_duplicates(char *src, char *dest)
{
    bool isFirst = false; // Check if it's the first element
    int i; // Go through the original set

    // myStr -- convert char to string
    // holder -- holding an element
    char myStr[2], holder[BUFSIZ];

    holder[0] = ','; 
    holder[1] = '\0';
    dest[0] = '\0';

    for (i = 0; i < strlen(src); i++) {
        if (src[i] == '{') { // Add open curly
            strcat(dest, "{\0");
            isFirst = true;

        } else if (src[i] == '}') {// Add close curly
            strcat(holder, ",\0");
            if (strstr(dest, holder) == NULL) {
                if (isFirst) // Then the string should be e.g. {,3,}
                    strcat(dest, holder);
                else // Concat from second char e.g. dest = {,1,} -> {,1,3,}
                    strcat(dest, holder+1);
            }
            strcat(dest, "}\0");

        } else if (src[i] == ',') { // One element end, check if it's in buffer
            strcat(holder, ",");
            if (strstr(dest, holder) == NULL) {
                if (isFirst) // Then the string should be e.g. {,3,}
                    strcat(dest, holder);
                else // Concat from second char e.g. dest = {,1,} -> {,1,3,}
                    strcat(dest, holder+1);
            }
            holder[0] = ',';
            holder[1] = '\0';
            isFirst = false;

        } else { 
            myStr[0] = src[i];
            myStr[1] = '\0';
            strcat(holder, myStr);
        }
    }
}


/*
 * Check if an element belongs to the set
 */
bool contains(int val, char *set)
{
    // length -- convert an int to string, malloc space
    // i -- helps to convert int to sting
    // absVal -- convert to absolute value
    int length, i, absVal;

    // result1/2/3 -- finding substring in different format
    // tmp -- holding different format of element
    // value -- holding val in string type
    char *result1, *result2, *result3, tmp[BUFSIZ], value[BUFSIZ];
    bool res = true;

    absVal = abs(val);
    value[0] = '\0';

    // Convert integer to char array
    if (val > 0) {
        length = (int)floor(log10((float)absVal))+1;
        i = length-1; 
        while (i >= 0){
            value[i--] = absVal%10+'0';
            absVal /= 10;
        }
        value[length] = '\0';
    } else if (val < 0) {
        length = (int)floor(log10((float)absVal))+2;
        i = length-1; 
        while (i >= 1){
            value[i--] = absVal%10+'0';
            absVal /= 10;
        }
        value[length] = '\0';
        value[0] = '-';
    } else {
        value[0] = '0';
        value[1] = '\0';
    }

    // Check if ",value," is in the set
    tmp[0] = ',';
    tmp[1] = '\0';
    strcat(tmp, value);
    strcat(tmp, ",\0");
    result1 = strstr(set, tmp);

    // Check if "{value," is in the set
    tmp[0] = '{';
    tmp[1] = '\0';
    strcat(tmp, value);
    strcat(tmp, ",\0");
    result2 = strstr(set, tmp);

    // Check if ",value}" is in the set
    tmp[0] = ',';
    tmp[1] = '\0';
    strcat(tmp, value);
    strcat(tmp, "}\0");
    result3 = strstr(set, tmp);

    if (result1 == NULL && result2 == NULL && result3 == NULL)
        res = false;

    return res;
}


/*
 * Check if set1 is a subset of set2
 */
bool isSubsetOf(char *set1, char *set2)
{
    // commaSet1/2 -- change the format of set1/2
    char commaSet1[BUFSIZ], commaSet2[BUFSIZ], tmpHolder[BUFSIZ];    
    int i, j;
    bool result = true;

    // Change set1 to  ...,value,value,value,  such format 
    for (j = 0, i = 1; i < strlen(set1); i++) {
        if (set1[i] == '}')
            commaSet1[j++] = ',';
        else
            commaSet1[j++] = set1[i];
    }
    commaSet1[j] = '\0';

    // Change set2 to  ,value,value,...,value, such format
    for (j = 0, i = 0; i < strlen(set2); i++) {
        if (set2[i] == '{')
            commaSet2[j++] = ',';
        else if (set2[i] == '}')
            commaSet2[j++] = ',';
        else
            commaSet2[j++] = set2[i];
    }
    commaSet2[j] = '\0';

    // Go through every element in commaSet1
    tmpHolder[0] = ',';
    for (i = 0, j = 1; i < strlen(commaSet1); i++) {
        if (commaSet1[i] == ',') {
            // This is where the value end
            // The whole value is in tmpholder, and then check if it's in set2
            tmpHolder[j++] = ',';
            tmpHolder[j] = '\0';
            // Now tmpHolder = ",value,"
            
            if (strstr(commaSet2, tmpHolder) == NULL) {
                result = false;
                break;
            }
            j = 1; // Clear tmpholder and reuse it to store next value
        } else
            tmpHolder[j++] = commaSet1[i];
    }

    return result;
}


/*
 * dest = set1 && set2
 */
void union_sets (char *set1, char *set2, char *dest)
{
    int i, j;
    char temp[strlen(set1)+strlen(set2)];

    if (strlen(set1) == 2) // set1 = {}
        remove_duplicates(set2, temp);
    else if (strlen(set2) == 2) // set2 = {}
        remove_duplicates(set1, temp);
    else { // Concat 2 sets and remove duplicates
        set1[strlen(set1)-1] = '\0';
        set2[0] = ',';
        strcat(set1, set2);
        remove_duplicates(set1, temp);
    }

    // Remove redundant commas
    for(i = 0, j = 0; temp[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp[i+1] == '}')
            dest[j++] = temp[i+1];
        else dest[j++] = temp[i];
    }
    dest[j] = '\0';
}


/*
 * dest = set1 || set2
 */
void intersection(char *set1, char *set2, char *dest)
{
    // Check if it's the first element, and if it's null set
    bool isFirst = false, nullSet = true;
    // holder -- holder element
    // myStr -- convert char to string
    char holder[BUFSIZ], myStr[2];
    int i;

    // Convert {} to commas
    set1[0] = ',';
    set2[0] = ',';
    set1[strlen(set1)-1] = ',';
    set2[strlen(set2)-1] = ',';

    holder[0] = ','; 
    holder[1] = '\0';
    dest[0] = ','; 
    dest[1] = '\0';

    for (i = 0; i < strlen(set2); i++) {
        if (set2[i] == ',') {
            if (!isFirst) // This is the first element
                isFirst = true;
            else {
                strcat(holder, ",\0");
                if (strstr(set1, holder) != NULL && !nullSet) {
                    dest[strlen(dest)-1] = '\0'; // Concat element to dest
                    strcat(dest, holder); 
                }
                holder[0] = ',';
                holder[1] = '\0';
            }
        } else {
            myStr[0] = set2[i];
            myStr[1] = '\0';
            strcat(holder, myStr);
            nullSet = false;
        }
    }

    dest[0] = '{';
    if (strlen(dest) == 1) { // Null set
        dest[1] = '}';
        dest[2] = '\0';
    } else {
        dest[strlen(dest)-1] = '}';
        dest[strlen(dest)] = '\0';
    }
}


/*
 * dest = set1 - set2
 */
void difference(char *set1, char *set2, char *dest)
{
    // Check if it's the first element
    bool firstEle = false;
    // holder -- holder element
    // myStr -- convert char to string
    char holder[BUFSIZ], myStr[2];
    int i;

    // Convert {} to commas
    set1[0] = ',';
    set2[0] = ',';
    set1[strlen(set1)-1] = ',';
    set2[strlen(set2)-1] = ',';

    holder[0] = ','; 
    holder[1] = '\0';
    dest[0] = ','; 
    dest[1] = '\0';

    for (i = 0; i < strlen(set1); i++) {
        if (set1[i] == ',') {
            if (!firstEle) // This is the first element
                firstEle = true;
            else {
                strcat(holder, ",\0");
                if (strstr(set2, holder) == NULL) {
                    dest[strlen(dest)-1] = '\0';
                    strcat(dest, holder);
                }
                holder[0] = ',';
                holder[1] = '\0';
            }
        } else {
            myStr[0] = set1[i];
            myStr[1] = '\0';
            strcat(holder, myStr);
        }
    }

    dest[0] = '{';
    if (strlen(dest) == 1) {
        dest[1] = '}';
        dest[2] = '\0';
    } else {
        dest[strlen(dest)-1] = '}';
        dest[strlen(dest)] = '\0';
    }
}


// Input function
PG_FUNCTION_INFO_V1(intset_in);

Datum intset_in(PG_FUNCTION_ARGS)
{
    char *src = PG_GETARG_CSTRING(0);

    // temp -- Hold array without space (but with duplicates)
    // temp2 -- Hold array without duplicates
    // buffer -- Hold final result
    char temp[strlen(src)], temp2[strlen(src)], *buffer;
    int i, j;

    isValid_changeFormat(src, temp);
    remove_duplicates(temp, temp2);

    buffer = (char *) palloc(sizeof(char) * strlen(temp2));
    for(i = 0, j = 0; temp2[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp2[i+1] == '}')
            buffer[j++] = temp2[i+1];
        else buffer[j++] = temp2[i];
    }
    buffer[j] = '\0';

    PG_RETURN_TEXT_P(cstring_to_text(buffer));
}


// Output function
PG_FUNCTION_INFO_V1(intset_out);

Datum intset_out(PG_FUNCTION_ARGS) 
{
    text *info = (text *)PG_GETARG_TEXT_P(0);

    PG_RETURN_CSTRING(text_to_cstring(info));
}


PG_FUNCTION_INFO_V1(intset_recv);

Datum intset_recv(PG_FUNCTION_ARGS) 
{
    StringInfo buf = (StringInfo) PG_GETARG_CSTRING(0);
    text *result = (text *) palloc(sizeof(text));
    strcpy(result->vl_dat, pq_getmsgstring(buf));

    PG_RETURN_TEXT_P(result);
}

PG_FUNCTION_INFO_V1(intset_send);


Datum intset_send(PG_FUNCTION_ARGS) 
{
    text *info = (text *) PG_GETARG_TEXT_P(0);
    StringInfoData buf;

    pq_begintypsend(&buf);
    pq_sendstring(&buf, info->vl_dat);

    PG_RETURN_BYTEA_P(pq_endtypsend(&buf));
}


// New operators

// operators: <@
PG_FUNCTION_INFO_V1(intset_contains);

Datum intset_contains(PG_FUNCTION_ARGS) 
{
    int val = PG_GETARG_INT32(0);
    char *src = text_to_cstring(PG_GETARG_TEXT_P(1));

    // temp -- Hold array without space (but with duplicates)
    // temp2 -- Hold array without duplicates
    // buffer -- Hold final result
    char temp[strlen(src)], temp2[strlen(src)], *buffer;
    int i, j;

    isValid_changeFormat(src, temp);
    remove_duplicates(temp, temp2);

    buffer = (char *) palloc(sizeof(char) * strlen(temp2));
    for(i = 0, j = 0; temp2[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp2[i+1] == '}')
            buffer[j++] = temp2[i+1];
        else buffer[j++] = temp2[i];
    }
    buffer[j] = '\0';

    PG_RETURN_BOOL(contains(val, buffer)); 
}


// operators: @
PG_FUNCTION_INFO_V1(intset_cardinality);

Datum intset_cardinality(PG_FUNCTION_ARGS) {

    char *src = text_to_cstring(PG_GETARG_TEXT_P(0));

    // temp -- Hold array without space (but with duplicates)
    // temp2 -- Hold array without duplicates
    // buffer -- Hold final result
    char temp[strlen(src)], temp2[strlen(src)], *buffer;
    int i, j, result = 0;

    isValid_changeFormat(src, temp);
    remove_duplicates(temp, temp2);

    buffer = (char *) palloc(sizeof(char) * strlen(temp2));
    for(i = 0, j = 0; temp2[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp2[i+1] == '}')
            buffer[j++] = temp2[i+1];
        else buffer[j++] = temp2[i];
    }
    buffer[j] = '\0';

    // card = #commas + 1 (for not null set)
    for (i = 0; i < strlen(buffer); i++)
        if (buffer[i] == ',')
            result++;
    if (strlen(buffer) > 2) result++; 

    PG_RETURN_INT32(result); 
}


// operators: @>
PG_FUNCTION_INFO_V1(intset_subset);

Datum intset_subset(PG_FUNCTION_ARGS) 
{
    char *src1 = text_to_cstring(PG_GETARG_TEXT_P(0));
    char *src2 = text_to_cstring(PG_GETARG_TEXT_P(1));

    // temp, temp3 -- Hold array without space (but with duplicates)
    // temp2, temp4 -- Hold array without duplicates
    // buffer1/2 -- Hold final result
    char temp[strlen(src1)], temp2[strlen(src1)], temp3[strlen(src2)], temp4[strlen(src2)], *buffer1, *buffer2;
    int i, j;

    isValid_changeFormat(src1, temp);
    remove_duplicates(temp, temp2);

    buffer1 = (char *) palloc(sizeof(char) * strlen(temp2));
    for(i = 0, j = 0; temp2[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp2[i+1] == '}')
            buffer1[j++] = temp2[i+1];
        else buffer1[j++] = temp2[i];
    }
    buffer1[j] = '\0';


    isValid_changeFormat(src2, temp3);
    remove_duplicates(temp3, temp4);

    buffer2 = (char *) palloc(sizeof(char) * strlen(temp4));
    for(i = 0, j = 0; temp4[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp4[i+1] == '}')
            buffer2[j++] = temp4[i+1];
        else buffer2[j++] = temp4[i];
    }
    buffer2[j] = '\0';


    PG_RETURN_BOOL(isSubsetOf(buffer1, buffer2)); 
}


// operators: =
PG_FUNCTION_INFO_V1(intset_equal);

Datum intset_equal(PG_FUNCTION_ARGS)
{
    char *src1 = text_to_cstring(PG_GETARG_TEXT_P(0));
    char *src2 = text_to_cstring(PG_GETARG_TEXT_P(1));

    // temp, temp3 -- Hold array without space (but with duplicates)
    // temp2, temp4 -- Hold array without duplicates
    // buffer1/2 -- Hold final result
    char temp[strlen(src1)], temp2[strlen(src1)], temp3[strlen(src2)], temp4[strlen(src2)], *buffer1, *buffer2;
    int i, j;

    isValid_changeFormat(src1, temp);
    remove_duplicates(temp, temp2);

    buffer1 = (char *) palloc(sizeof(char) * strlen(temp2));
    for(i = 0, j = 0; temp2[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp2[i+1] == '}')
            buffer1[j++] = temp2[i+1];
        else buffer1[j++] = temp2[i];
    }
    buffer1[j] = '\0';


    isValid_changeFormat(src2, temp3);
    remove_duplicates(temp3, temp4);

    buffer2 = (char *) palloc(sizeof(char) * strlen(temp4));
    for(i = 0, j = 0; temp4[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp4[i+1] == '}')
            buffer2[j++] = temp4[i+1];
        else buffer2[j++] = temp4[i];
    }
    buffer2[j] = '\0';

    PG_RETURN_BOOL(isSubsetOf(buffer1, buffer2) && isSubsetOf(buffer2, buffer1)); 
}


// operators: ||
PG_FUNCTION_INFO_V1(intset_union);

Datum intset_union(PG_FUNCTION_ARGS) 
{
    char *src1 = text_to_cstring(PG_GETARG_TEXT_P(0));
    char *src2 = text_to_cstring(PG_GETARG_TEXT_P(1));

    char tmp[strlen(src1)+strlen(src2)], *buffer;
    // temp, temp3 -- Hold array without space (but with duplicates)
    // temp2, temp4 -- Hold array without duplicates
    // buffer1/2 -- Hold final result
    char temp[strlen(src1)], temp2[strlen(src1)], temp3[strlen(src2)], temp4[strlen(src2)], *buffer1, *buffer2;
    int i, j;

    isValid_changeFormat(src1, temp);
    remove_duplicates(temp, temp2);

    buffer1 = (char *) palloc(sizeof(char) * strlen(temp2));
    for(i = 0, j = 0; temp2[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp2[i+1] == '}')
            buffer1[j++] = temp2[i+1];
        else buffer1[j++] = temp2[i];
    }
    buffer1[j] = '\0';


    isValid_changeFormat(src2, temp3);
    remove_duplicates(temp3, temp4);

    buffer2 = (char *) palloc(sizeof(char) * strlen(temp4));
    for(i = 0, j = 0; temp4[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp4[i+1] == '}')
            buffer2[j++] = temp4[i+1];
        else buffer2[j++] = temp4[i];
    }
    buffer2[j] = '\0';


    union_sets(buffer1, buffer2, tmp);

    buffer = (char *) palloc(sizeof(char) * strlen(tmp));
    buffer[0] = '\0';
    strcat(buffer, tmp);

    PG_RETURN_TEXT_P(cstring_to_text(buffer));
}


// operators: &&
PG_FUNCTION_INFO_V1(intset_intersection);

Datum intset_intersection(PG_FUNCTION_ARGS) 
{
    char *src1 = text_to_cstring(PG_GETARG_TEXT_P(0));
    char *src2 = text_to_cstring(PG_GETARG_TEXT_P(1));

    char tmp[strlen(src1)+strlen(src2)], *buffer;
    // temp, temp3 -- Hold array without space (but with duplicates)
    // temp2, temp4 -- Hold array without duplicates
    // buffer1/2 -- Hold final result
    char temp[strlen(src1)], temp2[strlen(src1)], temp3[strlen(src2)], temp4[strlen(src2)], *buffer1, *buffer2;
    int i, j;

    isValid_changeFormat(src1, temp);
    remove_duplicates(temp, temp2);

    buffer1 = (char *) palloc(sizeof(char) * strlen(temp2));
    for(i = 0, j = 0; temp2[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp2[i+1] == '}')
            buffer1[j++] = temp2[i+1];
        else buffer1[j++] = temp2[i];
    }
    buffer1[j] = '\0';


    isValid_changeFormat(src2, temp3);
    remove_duplicates(temp3, temp4);

    buffer2 = (char *) palloc(sizeof(char) * strlen(temp4));
    for(i = 0, j = 0; temp4[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp4[i+1] == '}')
            buffer2[j++] = temp4[i+1];
        else buffer2[j++] = temp4[i];
    }
    buffer2[j] = '\0';


    intersection(buffer1, buffer2, tmp);

    buffer = (char *) palloc(sizeof(char) * strlen(tmp));
    buffer[0] = '\0';
    strcat(buffer, tmp);

    PG_RETURN_TEXT_P(cstring_to_text(buffer));
}


// operators: -
PG_FUNCTION_INFO_V1(intset_difference);

Datum intset_difference(PG_FUNCTION_ARGS) 
{
    char *src1 = text_to_cstring(PG_GETARG_TEXT_P(0));
    char *src2 = text_to_cstring(PG_GETARG_TEXT_P(1));

    char tmp[strlen(src1)+strlen(src2)], *buffer;
    // temp, temp3 -- Hold array without space (but with duplicates)
    // temp2, temp4 -- Hold array without duplicates
    // buffer1/2 -- Hold final result
    char temp[strlen(src1)], temp2[strlen(src1)], temp3[strlen(src2)], temp4[strlen(src2)], *buffer1, *buffer2;
    int i, j;

    isValid_changeFormat(src1, temp);
    remove_duplicates(temp, temp2);

    buffer1 = (char *) palloc(sizeof(char) * strlen(temp2));
    for(i = 0, j = 0; temp2[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp2[i+1] == '}')
            buffer1[j++] = temp2[i+1];
        else buffer1[j++] = temp2[i];
    }
    buffer1[j] = '\0';


    isValid_changeFormat(src2, temp3);
    remove_duplicates(temp3, temp4);

    buffer2 = (char *) palloc(sizeof(char) * strlen(temp4));
    for(i = 0, j = 0; temp4[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp4[i+1] == '}')
            buffer2[j++] = temp4[i+1];
        else buffer2[j++] = temp4[i];
    }
    buffer2[j] = '\0';


    difference(buffer1, buffer2, tmp);

    buffer = (char *) palloc(sizeof(char) * strlen(tmp));
    buffer[0] = '\0';
    strcat(buffer, tmp);

    PG_RETURN_TEXT_P(cstring_to_text(buffer));
}


// operators: !!
PG_FUNCTION_INFO_V1(intset_disjunction);

Datum intset_disjunction(PG_FUNCTION_ARGS) 
{
    char *src1 = text_to_cstring(PG_GETARG_TEXT_P(0));
    char *src2 = text_to_cstring(PG_GETARG_TEXT_P(1));


    char temp_union[strlen(src1)+strlen(src2)], temp_intersc[strlen(src1)+strlen(src2)], temp_1[strlen(src1)+strlen(src2)], temp_2[strlen(src1)+strlen(src2)], *buffer1, *buffer2, *buffer3, *buffer4;

    // temp, temp3 -- Hold array without space (but with duplicates)
    // temp2, temp4 -- Hold array without duplicates
    // buffer1/2 -- Hold final result
    char temp[strlen(src1)], temp2[strlen(src1)], temp3[strlen(src2)], temp4[strlen(src2)], *buff1, *buff2;
    int i, j;

    isValid_changeFormat(src1, temp);
    remove_duplicates(temp, temp2);

    buff1 = (char *) palloc(sizeof(char) * strlen(temp2));
    for(i = 0, j = 0; temp2[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp2[i+1] == '}')
            buff1[j++] = temp2[i+1];
        else buff1[j++] = temp2[i];
    }
    buff1[j] = '\0';


    isValid_changeFormat(src2, temp3);
    remove_duplicates(temp3, temp4);

    buff2 = (char *) palloc(sizeof(char) * strlen(temp4));
    for(i = 0, j = 0; temp4[i] != '}'; i++) {
        if (i == 1) continue;
        else if (temp4[i+1] == '}')
            buff2[j++] = temp4[i+1];
        else buff2[j++] = temp4[i];
    }
    buff2[j] = '\0';


    // buffer1 = intersection
    intersection(buff1, buff2, temp_intersc);
    buffer1 = (char *) palloc(sizeof(char) * (strlen(temp_intersc)));
    buffer1[0] = '\0';
    strcat(buffer1, temp_intersc);

    // buffer2 = buff1 - buffer1
    difference(buff1, buffer1, temp_1);
    buffer2 = (char *) palloc(sizeof(char) * (strlen(temp_1)));
    buffer2[0] = '\0';
    strcat(buffer2, temp_1);

    // buffer3 = buff2 - buffer1
    difference(buff2, buffer1, temp_2);
    buffer3 = (char *) palloc(sizeof(char) * (strlen(temp_2)));
    buffer3[0] = '\0';
    strcat(buffer3, temp_2);

    // buffer4 = buffer2 || buffer3
    union_sets(buffer2, buffer3, temp_union);
    buffer4 = (char *) palloc(sizeof(char) * (strlen(temp_union)));
    buffer4[0] = '\0';
    strcat(buffer4, temp_union);

    PG_RETURN_TEXT_P(cstring_to_text(buffer4));
}
