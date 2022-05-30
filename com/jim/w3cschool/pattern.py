import re

'''
.	匹配除 "\n" 之外的任何单个字符。要匹配包括 '\n' 在内的任何字符，请使用象 '[.\n]' 的模式。
\d	匹配一个数字字符。等价于 [0-9]。
\D	匹配一个非数字字符。等价于 [^0-9]。
\s	匹配任何空白字符，包括空格、制表符、换页符等等。等价于 [ \f\n\r\t\v]。
\S	匹配任何非空白字符。等价于 [^ \f\n\r\t\v]。
\w	匹配包括下划线的任何单词字符。等价于'[A-Za-z0-9_]'。
\W	匹配任何非单词字符。等价于 '[^A-Za-z0-9_]'。

re.match 只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回 None；而 re.search 匹配整个字符串，直到找到一个匹配。
'''

line = "Cats are smarter than dogs"
pattern = r'(.*) are (.*?) .*'

# 0.1
matchObj1 = re.match("www", "www.w3cschool.cn")
print(matchObj1)
print(matchObj1.span())
print(matchObj1.group())
print('--------------------------------------------------------\n')

# 0.2

'''
re.I	使匹配对大小写不敏感
re.L	做本地化识别（locale-aware）匹配
re.M	多行匹配，影响 ^ 和 $
re.S	使 . 匹配包括换行在内的所有字符
re.U	根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.
re.X	该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。
'''

matchObj2 = re.match(pattern, line, re.MULTILINE | re.IGNORECASE)
if matchObj2:
    print("matchObj : ", matchObj2)
    print("matchObj.group() : ", matchObj2.group())
    print("matchObj.group(1) : ", matchObj2.group(1))
    print("matchObj.group(2) : ", matchObj2.group(2))
else:
    print("No match!!")

print('--------------------------------------------------------\n')

matchObj31 = re.search('www', 'www.w3cschool.cn')
print(matchObj31)
print(matchObj31.span())
matchObj32 = re.search('cn', 'www.w3cschool.cn')
print(matchObj32)
print(matchObj32.span())

print('--------------------------------------------------------\n')

searchObj1 = re.search(pattern, line, re.M | re.I)

if searchObj1:
    print("searchObj : ", searchObj1)
    print("searchObj.group() : ", searchObj1.group())
    print("searchObj.group(1) : ", searchObj1.group(1))
    print("searchObj.group(2) : ", searchObj1.group(2))
else:
    print("Nothing found!!")

print('--------------------------------------------------------\n')

phone = "2004-959-559 # 这是一个电话号码"

# 删除注释
num = re.sub(r'#.*$', "", phone)
print("电话号码 : ", num)

# 移除非数字的内容
num = re.sub(r'\D', "", phone)
print("电话号码 : ", num)
