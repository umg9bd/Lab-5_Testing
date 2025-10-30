1.	Which issues were the easiest to fix, and which were the hardest? Why?
The easiest ones to fix were the formatting and style errors,things like missing blank lines, missing docstrings, or unused imports. They didn’t require much thought, just following PEP 8 rules. The hardest one was the raise-missing-from warning. I had to actually understand why it mattered and how exception chaining works in Python.

2.	Did the static analysis tools report any false positives? If so, describe one example.
Using a global variable felt like a bit of a false positive. In this small script, having a module-level stock_data dictionary was intentional and didn’t really cause problems but the tool flagged it anyway.

3.	How would you integrate static analysis tools into your actual software development workflow? Consider continuous integration (CI) or local development practices.
I’d probably set them up to run automatically before committing changes. Using a pre-commit hook or adding them to a CI pipeline makes sense so that code can’t be merged unless it passes the checks.I’d also keep running pylint or flake8 locally while coding, just to catch stuff early instead of being hit with 20 warnings later. It’s easier to fix small things as you go than to clean up a a lot at the end.

4.	What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?
After cleaning everything up, the code looks and feels more professional. The functions have proper names, consistent formatting, and clear docstrings that explain what’s going on.
The file handling and exception updates made the code safer and less likely to break. It’s also just easier to read now and flows better, and nothing feels sloppy or confusing. Overall, it feels like something I’d be comfortable showing to someone else.

