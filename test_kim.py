
import kim as k

def test_url_to_md():
    url = "This is my link http://a/b/c/g;x?y#s and good it is https://a.com"
    url = "bhttp://a/b/c/g;x?y#s and urls start with http:// like that"
    #assert k.url_to_md(url) == "This is my link [http://www.test.com/data?values=123](http://www.test.com/data?values=123) and good it is [https://a.com](https://a.com)"
    j = k.url_to_md(url)
    assert j == "b[http://a/b/c/g;x?y#s](http://a/b/c/g;x?y#s) and urls start with http:// like that"

'''
References
https://medium.com/worldsensing-techblog/tips-and-tricks-for-unit-tests-b35af5ba79b1
'''