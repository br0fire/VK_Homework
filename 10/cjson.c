#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#include <Python.h>

#define MAX_JSON_SIZE 1024
#define MAX_BUFFER_SIZE 100000

typedef enum {
    JSON_STRING,
    JSON_NUMBER
} JsonValueType;

typedef struct {
    char* key;
    JsonValueType type;
    union {
        char* string;
        int number;
    } value;
} JsonPair;

int parseJson(const char* json, JsonPair* pairs) {
    int i = 0;
    // JsonPair pairs[MAX_JSON_SIZE];
    int pairCount = 0;
    char *key = NULL;
    while (json[i] != '{' && json[i] != '\0') {
            if (json[i] != ' ') {
            //   fprintf(stderr, "%c\n", json[i]);
            //    fprintf(stderr, "1");
                return -1;
            }
            i++;
    }
    if (json[i] == '\0') {
            fprintf(stderr, "ERROR: Expected {\n");
            return -1;
    }
    i++;
    while (json[i] != '\0') {
 
        while (json[i] != '\"' && json[i] != '\0') {
            if (json[i] != ' ') {
              //  fprintf(stderr, "2");
                return -1;
            }
            i++;
        }
        if (json[i] == '\0') {
            fprintf(stderr, "ERROR: Expected left \" in key\n");
            return -1;
        }
        i++;
        int keyStart = i;
        while (json[i] != '\"' && json[i] != '\0') {
            i++;
        }
        if (json[i] == '\0') {
            fprintf(stderr, "ERROR: Expected right \" in key\n");
            return -1;
        }
        int keyEnd = i - 1;
        int keyLength = keyEnd - keyStart + 1;
        key = malloc(keyLength + 1);
        strncpy(key, json+keyStart, keyLength);
        key[keyLength] = '\0';
        i++;
        while (json[i] != ':' && json[i] != '\0') {
            if (json[i] != ' ') {
                //fprintf(stderr, "3");
                return -1;
            }
            i++;
        }
        if (json[i] == '\0') {
            fprintf(stderr, "ERROR: Expected :\n");
            return -1;
        }
        i++;
        while ((json[i] != '\"' && !isdigit(json[i]) ) && json[i] != '\0') {
            if (json[i] != ' ') {
                // fprintf(stderr, "%c\n", json[i]);
              //  fprintf(stderr, "4");
                return -1;
            }
            i++;
        }
        if (json[i] == '\0') {
            fprintf(stderr, "ERROR: Expected left \" or digit\n");
            return -1;
        } 
        if (json[i] == '\"') {
            i++;
            int valueStart = i;
            while (json[i] != '\"' && json[i] != '\0') {
                i++;
            }
            if (json[i] == '\0') {
                fprintf(stderr, "ERROR: Expected right \" in value\n");
                return -1;
            }
            int valueEnd = i - 1;
            int valueLength = valueEnd - valueStart + 1;
            char* value = malloc(valueLength + 1);
            strncpy(value, json+valueStart, valueLength);
            value[valueLength] = '\0';
            // printf("Key: %s Value: %s\n", key, value);
            pairs[pairCount].key = key;
            pairs[pairCount].type = JSON_STRING;
            pairs[pairCount].value.string = value;
            pairCount++;
            i++;
        }
            // Check if the value is a number
        else if (isdigit(json[i])) {
            int value = 0;
            while (isdigit(json[i])) {
                value = value * 10 + (json[i] - '0');
                i++;
            }
            pairs[pairCount].key = key;
            pairs[pairCount].type = JSON_NUMBER;
            pairs[pairCount].value.number = value;
            pairCount++;
        }
        while ((json[i] != ',' && json[i] != '}') && json[i] != '\0') {
            if (json[i] != ' ') {
                //  fprintf(stderr, "5");
                return -1;
            }
            i++;
        }
        if (json[i] == '\0') {
            fprintf(stderr, "ERROR: Expected , or }\n");
            return -1;
        } 
        i++;
    }
    return pairCount;
}

PyObject* cjson_loads(PyObject* self, PyObject* args) {
    char* json_str;
    if(!PyArg_ParseTuple(args, "s", &json_str))
    {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }

    PyObject *dict = NULL;
    if (!(dict = PyDict_New())) {
        printf("ERROR: Failed to create Dict Object\n");
        return NULL;
    }

    JsonPair pairs[MAX_JSON_SIZE];
    long pairCount = 0;
    pairCount = parseJson(json_str, pairs);
    if (pairCount == -1) {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }
    PyObject *key = NULL;
    PyObject *value = NULL;
    for (int j = 0; j < pairCount; j++) {
        
        if (!(key = Py_BuildValue("s", pairs[j].key))) {
            printf("ERROR: Failed to build string value\n");
            return NULL;
        }

        if (pairs[j].type == JSON_STRING) {
            if (!(value = Py_BuildValue("s", pairs[j].value.string))) {
                printf("ERROR: Failed to build string value\n");
                return NULL;
            }
        } else if (pairs[j].type == JSON_NUMBER) {
            if (!(value = Py_BuildValue("i", pairs[j].value.number))) {
                printf("ERROR: Failed to build integer value\n");
                return NULL;
            }
        }
        if (PyDict_SetItem(dict, key, value) < 0) {
            printf("ERROR: Failed to set item\n");
            return NULL;
        }
    }
    if (PyDict_Size(dict) == 0) {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }
    return dict;
}

void append_string(char *json, const char *str) {
    strcat(json, "\"");
    strcat(json, str);
    strcat(json, "\"");
}

int append_key_value(char *json, const char *key, PyObject *value, int* offset) {
    (*offset) += snprintf(json + *offset, MAX_BUFFER_SIZE - *offset, "\"%s\":", key);
    json[(*offset)++] = ' ';
    long temp = 0;
    if (PyLong_Check(value)) {
        temp = PyLong_AsLong(value);
       (*offset) += snprintf(json + *offset, MAX_BUFFER_SIZE - *offset, "%ld", temp);
    } else {
        PyObject* str = PyUnicode_AsEncodedString(value, "utf-8", "~E~");
        if (!str) {
            PyErr_Format(PyExc_TypeError, "Expected object or value");
            return -1;
        }
        const char *bytes = PyBytes_AS_STRING(str);
        if (!bytes) {
            PyErr_Format(PyExc_TypeError, "Expected object or value");
            return -1;
        }
        (*offset) += snprintf(json + *offset, MAX_BUFFER_SIZE - *offset, "\"%s\"", bytes);
    }
    return 1;
}

PyObject* cjson_dumps(PyObject* self, PyObject* args){
    PyObject* dict_obj;
    if(!PyArg_ParseTuple(args, "O", &dict_obj))
    {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }
    if (!PyDict_Check(dict_obj)) {
        PyErr_Format(PyExc_TypeError, "Expected object or value");
        return NULL;
    }
    PyObject *key, *value;
    Py_ssize_t pos = 0;
    char json[MAX_BUFFER_SIZE];
    int offset = 0;
    json[offset++] = '{';


    while (PyDict_Next(dict_obj, &pos, &key, &value)) {
        PyObject* str = PyUnicode_AsEncodedString(key, "utf-8", "~E~");
        if (!str) {
            PyErr_Format(PyExc_TypeError, "Expected object or value");
            return NULL;
        }
        const char *bytes = PyBytes_AS_STRING(str);
        if (!bytes) {
            PyErr_Format(PyExc_TypeError, "Expected object or value");
            return NULL;
        }
        if (append_key_value(json, bytes, value, &offset) == -1) {
            return NULL;
        }

        json[offset++] = ',';
        json[offset++] = ' ';

        
    }
    offset--;
    offset--;

    json[offset++] = '}';
    json[offset] = '\0';
    return Py_BuildValue("s", json);
}


static PyMethodDef methods[] = {
    {"loads", cjson_loads, METH_VARARGS, "Parse the json"},
    {"dumps", cjson_dumps, METH_VARARGS, "Dumps to json"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cjsonmodule = {
    PyModuleDef_HEAD_INIT,
    "cjson",
    "Module for my first c api code.",
    -1,
    methods
};

PyMODINIT_FUNC PyInit_cjson(void)
{
    return PyModule_Create( &cjsonmodule );
}
