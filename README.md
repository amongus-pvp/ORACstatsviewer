# ORACstatsviewer
Stats viewer for ORAC users

To use this, you first need to run `main.py`. It will ask for your cookies header. Here is how to do this:

1. Log in to your ORAC account
2. Go to https://orac2.info/hub/allsubs/1
3. Inspect Element → go to the Network tab
4. Refresh the page
5. Click the request to `1`
6. Find the section under `Request Headers`
7. Copy everything next to `Cookies: ` (this should come in the form: `csrftoken=SOMETHING; sessionid=SOMETHING`)

Input the the max page number `ORAC` will say something like `Page 1 of X`, just input `X`.

After this is done, run the `stats.py` file and look at the cool data.
So far here is what I've been able to do:
1. Cumulative graph of submissions over time
2. Solving a problem is highlighted in green on this graph
3. A histogram is displayed of when your submissions appear most
4. A frequency table is provided for which problems you submit to the most

There is more coming I promise!
