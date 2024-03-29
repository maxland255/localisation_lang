# LocalLang

**Installation**

```commandline
pip install local-lang
```

**Example**


`test.py`

```python
from locallang import LangInit
import datetime

localisation = LangInit()

local = localisation.getLocalisation(lang="en_us")

print(local.hey())
print(local.hello_world())
print(local.toDay(date=datetime.datetime.now()))
print(local.thisTime(time=datetime.datetime.now().time()))
print(local.testStr(strText="Hello world!"))
print(local.testInt(intNum=1))
print(local.testFloat(floatNum=1.5))
print(local.testBool(boolValue=True))
print(local.test(test=1.5))

local = localisation.getLocalisation(lang="fr")

print(local.hey())
print(local.hello_world())
print(local.toDay(date=datetime.datetime.now()))
print(local.thisTime(time=datetime.datetime.now().time()))
print(local.testStr(strText="Bonjour tout le monde !"))
print(local.testInt(intNum=2))
print(local.testFloat(floatNum=2.5))
print(local.testBool(boolValue=False))
print(local.test(test="coucou"))
```

`en_us.json`
```json
{
    "hey": "Hey!",
    "hello_world": "Hello world!",
    "toDay": "Date: {date}",
    "@toDay": {
        "placeholders": {
            "date": {
                "type": "datetime",
                "format": "%Y/%m/%d %H:%M"
            }
        }
    },
    "thisTime": "Time: {time}",
    "@thisTime": {
        "placeholders": {
            "time": {
                "type": "time",
                "format": "%H:%M"
            }
        }
    },
    "testStr": "Test: {strText}",
    "@testStr": {
        "placeholders": {
            "strText": {
                "type": "str"
            }
        }
    },
    "testInt": "Test: {intNum}",
    "@testInt": {
        "placeholders": {
            "intNum": {
                "type": "int"
            }
        }
    },
    "testFloat": "Test: {floatNum}",
    "@testFloat": {
        "placeholders": {
            "floatNum": {
                "type": "float"
            }
        }
    },
    "testBool": "Test: {boolValue}",
    "@testBool": {
        "placeholders": {
            "boolValue": {
                "type": "bool"
            }
        }
    },
    "test": "Test: {test}"
}
```

`fr.json`
```json
{
    "hey": "Coucou !",
    "hello_world": "Bonjour tout le monde!",
    "toDay": "Date: {date}",
    "thisTime": "Time: {time}",
    "testStr": "Test: {strText}",
    "testInt": "Test: {intNum}",
    "testFloat": "Test: {floatNum}",
    "testBool": "Test: {boolValue}",
    "test": "Test: {test}"
}
```

`result in consol`
```text
Hey!
Hello world!
Date: 2023/05/07 00:15
Time: 00:15
Test: Hello world!
Test: 1
Test: 1.5
Test: True
Test: 1.5
Coucou !
Bonjour tout le monde!
Date: 2023/05/07 00:15
Time: 00:15
Test: Bonjour tout le monde !
Test: 2
Test: 2.5
Test: False
Test: coucou
```
