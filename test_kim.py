
import kim as k

def test_url_to_md():
    url = "This is my link http://a/b/c/g;x?y#s and good it is https://a.com"
    url = "bhttp://a/b/c/g;x?y#s and urls start with http:// like that"
    #assert k.url_to_md(url) == "This is my link [http://www.test.com/data?values=123](http://www.test.com/data?values=123) and good it is [https://a.com](https://a.com)"
    j = k.url_to_md(url)
    assert j == "b[http://a/b/c/g;x?y#s](http://a/b/c/g;x?y#s) and urls start with http:// like that"


#not complete
def test_keep_note_name():
    ndate = "2021-06-12 180157-072000"
    k.keep_name_list = ["abc", "def", "ghi", "", "j", "mnopqr-stuvw", "xyz"]
    
    for name in k.keep_name_list:
       assert k.keep_note_name(name, ndate)  == name + ndate
    
    k.keep_name_list.append("abc"+ndate)
    assert k.keep_note_name("abc", ndate) == "abc"+ndate+ndate
    
    k.keep_name_list.remove("abc"+ndate)
    k.keep_name_list = []
    for name in k.keep_name_list:
        assert k.keep_note_name(name, ndate) == name


'''
References
https://medium.com/worldsensing-techblog/tips-and-tricks-for-unit-tests-b35af5ba79b1
'''