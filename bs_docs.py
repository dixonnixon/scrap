#get all class attributes in a list
get_attribute_list('class')

target_list = []
"""!!!Find matcing classes"""
for tag in bs.find_all("div"):
    if tag.has_attr('class'):
        # print("classes",tag.get_attribute_list('class'))
        classes = tag.get_attribute_list('class')
        matches = [match for match in classes if "post" in match]
        if len(matches) > 0:
            target_list.append(tag)


"""ls = ['Hello from AskPython', 'Hello', 'Hello boy!', 'Hi']
 
if any("AskPython" in word for word in ls):
    print('\'AskPython\' is there inside the list!')
else:
    print('\'AskPython\' is not there inside the list')
    


    ls = ['Hello from AskPython', 'Hello', 'Hello boy!', 'Hi']
 
# The second parameter is the input iterable
# The filter() applies the lambda to the iterable
# and only returns all matches where the lambda evaluates
# to true
filter_object = filter(lambda a: 'AskPython' in a, ls)
 
# Convert the filter object to list
print(list(filter_object))    
    
"""
