import re

testExpression = re.compile(r'\d{1,}\.\d{2}\Z')
testExpression2 = re.compile(r'\d{1,}\.\d{1}\Z')
testExpression3 = re.compile(r'\d{1,}\Z')


if testExpression3.match('192'):
    print('True')
else:
    print('False')