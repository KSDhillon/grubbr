# grubbr.io

CS 4501 Project
Group Members: Aadil Abbas, Karan Dhillon, Dan Kramp

#TODO
-for test cases, make sure to test for errors as well (passing in
invalid data).
(-1 point)

-Should have validation on both sides of every pipeline
(exp->web, models -> exp, etc.), at least checking status
codes to make sure one of the services didn’t fail.
(-2 points)

-Id recommend abstracting out your GET and POST request functions to
other layers so you don’t have to do the encode/decode json stuff
in every view

-Your EXP layer is supposed to be reflective of an entire
page/experience of your site. For example, you should have a home
page service that gathers all the data that your home page may need
(popular items, user info, etc., instead of get_item and get_items
that you currently have)
(-2 points)

-Instead of using template.render() in your web views, you can use
the shortcut render() function that django provides that takes in a
request, the template name, and the context dict you want to
pass.
