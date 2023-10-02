# student_management_system_in_django


<hr>
<h2>Installation Steps : </h2>

<p>Project Dependency :</p>
<pre>
pip install requests
pip install Django
pip install mysql-client
pip install mysqlclient
</pre>
<hr>
<ul>
<ol>First Create MySql Database Tutorial : <a href="https://youtu.be/cEazlDKu86E">https://youtu.be/cEazlDKu86E</a> </ol>
<ol>Change Database Setting in settings.py </ol>
<ol>
Run Migration Command 
<pre>
python manage.py makemigrations
python manage.py migrate
</pre>
 <ul>     
<li>In login_page.html Replace <pre>CAPTCHA_CLIENT_KEY</pre> with Captcha Client Side Key</li>
<li>In views.py Replace <pre>CAPTCHA_SERVER_KEY</pre> with Captcha SERVER Side Key</li>
<li>For Captcha Key Visit <a href="https://www.google.com/recaptcha/intro/v3.html">https://www.google.com/recaptcha/intro/v3.html</a></li>
</ul>
</ol>
<ol>
Run Project python runserver
</ol>
</ul>
<hr>


