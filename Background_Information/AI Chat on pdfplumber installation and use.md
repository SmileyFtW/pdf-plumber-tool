Using **pdfplumber** gives you precise control to fix the "split row" issue programmatically.  Unlike Power Query, you can write logic to detect when a row is a "continuation" (e.g., the first column is null) and merge it with the previous row before exporting.

Here is the step-by-step implementation:

# 1 1. Installation

Install the library via terminal/command prompt:

pip install pdfplumber pandas

# 2 2. The Python Script

This script extracts the table, identifies split rows (where the ID/Key column is null), and merges them into a single record.

import pdfplumber

import pandas as pd

pdf\_path = "your\_file.pdf"

all\_rows = []

# 1. Extract Raw Data

with pdfplumber.open(pdf\_path) as pdf:

for page in pdf.pages:

# Use 'lines' strategy to detect borders, or 'text' if no borders exist

table = page.extract\_table(table\_settings={

"vertical\_strategy": "lines",

"horizontal\_strategy": "lines",

"snap\_tolerance": 4,

"join\_tolerance": 4

})

if table:

# Skip header row if present on every page (adjust index as needed)

all\_rows.extend(table[1:] if page == pdf.pages[0] else table)

# 2. Convert to DataFrame

# Replace 'None' with empty strings for easier handling

df = pd.DataFrame(all\_rows).fillna('')

# 3. Define the Key Column

# This is the column that should ONLY have data on the first row of an entry

# Usually column 0 (e.g., Invoice ID, Item Code, Date)

key\_col\_index = 0

# 4. Create a Grouping Key

# Logic: If the key column has text, it's a NEW record (use its index).

# If it's empty, it's a continuation of the previous record.

df['group\_id'] = df[key\_col\_index].apply(lambda x: 1 if x.strip() != '' else 0).cumsum()

# 5. Merge Rows

# Group by the generated ID and combine text columns

def combine\_text(series):

# Filter out empty strings and join with a space

return " ".join([str(x).strip() for x in series if str(x).strip() != ''])

# Apply combination to ALL columns

# For numeric columns that only appear on the first row, you might use 'first' instead

aggregated\_df = df.groupby('group\_id').agg(lambda x: combine\_text(x)).reset\_index(drop=True)

# 6. Export to Excel/CSV

aggregated\_df.to\_excel("cleaned\_data.xlsx", index=False)

print("Extraction complete. File saved as 'cleaned\_data.xlsx'")

# 3 Key Logic Explained

- extract\_table Settings: Using "vertical\_strategy": "lines" tells pdfplumber to look for actual drawn lines in the PDF. If your PDF has no lines (white space only), change this to "text".
- cumsum() Trick: This creates a running count. Every time a row has a valid ID (e.g., "Inv-101"), the count increases by 1. Rows with null IDs get the same count as the row above them. This effectively tags all split rows with the same "Group ID".
- combine\_text: This function iterates through the split rows for a specific group, ignores empty cells, and joins the text with a space. This reconstructs the full description automatically.

# 4 Advanced: Handling Complex Layouts

If the standard extract\_table fails because the PDF layout is irregular (e.g., no grid lines), you can extract words directly and reconstruct rows based on Y-coordinates:

# Alternative for unstructured PDFs

with pdfplumber.open(pdf\_path) as pdf:

page = pdf.pages[0]

words = page.extract\_words()

# Sort words by vertical position (top to bottom), then horizontal

# Logic: If two words have very similar 'top' coordinates, they are on the same line.

# If a line has no text in the first column's X-range, it's a continuation.

[Python pdfplumber extract table merge rows tutorial](https://search.brave.com/videos?q=Python%20pdfplumber%20extract%20table%20merge%20rows%20tutorial)

**View all**

[pdfplumber extract\_table table\_settings merged cells python](https://search.brave.com/search?q=pdfplumber%20extract_table%20table_settings%20merged%20cells%20python)

**View all**

**Copy**

I am using VS Code for python projects. Provide step by step using VS Code

Finished

Here is the step-by-step workflow to run the pdfplumber script in Visual Studio Code (VS Code), ensuring your environment is correctly configured to avoid import errors.

# 5 1. Install the Python Extension

If you haven't already, enable full Python support:

- Click the Extensions icon on the left sidebar (or press Ctrl+Shift+X).
- Search for Python (published by Microsoft).
- Click Install. This enables IntelliSense, linting, and terminal integration.

# 6 2. Create a Virtual Environment (Recommended)

Isolating dependencies prevents conflicts with other projects.

- Open the Command Palette (Ctrl+Shift+P or Cmd+Shift+P on Mac).
- Type and select Python: Create Environment.
- Select Venv and choose your preferred Python version.
- VS Code will create a .venv folder and automatically select it as your interpreter. You will see the environment name (e.g., ('.venv': venv)) in the bottom-left status bar.

# 7 3. Install pdfplumber in the VS Code Terminal

Crucially, you must install the package **inside** the virtual environment VS Code just created.

- Open the integrated terminal: Terminal > New Terminal (or press Ctrl+`).
- Verify Activation: Ensure the terminal prompt starts with (.venv) or similar. If not, the wrong interpreter is active.
- Run the installation command:

pip install pdfplumber pandas

*(Note: If pip is not recognized, try python -m pip install pdfplumber pandas)*.

# 8 4. Create and Run the Script

- Create a new file named extract\_pdf.py.
- Paste the Python code provided in the previous step into this file.
- Update the File Path: Change pdf\_path = "your\_file.pdf" to the actual path of your PDF (e.g., pdf\_path = "./data/invoice.pdf").
- Run the Script:
- Click the Play button (▶) in the top-right corner of the editor.
- Or right-click anywhere in the code and select Run Python File in Terminal.

# 9 Troubleshooting: "ModuleNotFoundError"

If you see an error saying No module named 'pdfplumber':

1. Check the Interpreter: Press Ctrl+Shift+P, type Python: Select Interpreter, and ensure the one with ('.venv') or your specific environment name is selected.
2. Re-install: With the correct interpreter selected, open the terminal and run pip install pdfplumber again. The package must be installed in the same environment that is running the script.

[Run Python script in VS Code with virtual environment](https://search.brave.com/videos?q=Run%20Python%20script%20in%20VS%20Code%20with%20virtual%20environment)

**View all**

[VS Code Python select interpreter fix ModuleNotFoundError](https://search.brave.com/search?q=VS%20Code%20Python%20select%20interpreter%20fix%20ModuleNotFoundError)

**View all**

**Copy**

I have my repos in a directory: C:\Users\UserName\GitRepos. I segregate the repos in their own directory: C:\Users\UserName\GitRepos\AppropriateDirectoryName. Should I create a folder for pdfplumber and be in that directory when I create the virtual environment?

Finished

**Yes, you should create a dedicated folder for your script inside your Git repos directory and create the virtual environment there.**

Given your structure (C:\Users\UserName\GitRepos\AppropriateDirectoryName), here is the recommended workflow:

# 10 1. Create a Project Folder

Since your PDF script is a distinct tool, give it its own repository folder. This keeps your GitRepos directory organized.

- Path: C:\Users\UserName\GitRepos\pdf-plumber-tool
- Action: Create this folder and open it in VS Code (File > Open Folder).

# 11 2. Create the Virtual Environment Inside This Folder

Once inside the new folder in VS Code:

- Open the terminal (Ctrl+ `).
- Run:

python -m venv .venv

- Why inside?
- VS Code Auto-Detection: VS Code automatically finds .venv in the root of your open folder and suggests it as the interpreter.
- Portability: If you move or copy this repo to another computer, the setup instructions (pip install -r requirements.txt) remain valid relative to the project.
- Isolation: Each tool in your GitRepos directory will have its own isolated dependencies, preventing version conflicts.

# 12 3. Critical Step: Ignore the Environment in Git

Since you are using Git, you **must** prevent the virtual environment (which contains thousands of system-specific files) from being committed to your repository.

- Create a file named .gitignore in the root of pdf-plumber-tool.
- Add this line to it:

.venv/

- Note: If you don't do this, you risk accidentally committing gigabytes of unnecessary data to your repo.

# 13 Summary of Recommended Structure

Your final directory structure should look like this:

C:\Users\UserName\GitRepos\

└── pdf-plumber-tool/ <-- Your new repo folder

├── .venv/ <-- Virtual environment (IGNORED by Git)

├── .gitignore <-- Contains ".venv/"

├── extract\_pdf.py <-- Your Python script

└── requirements.txt <-- List of dependencies (pdfplumber, pandas)

**Workflow**:

1. Navigate to C:\Users\UserName\GitRepos\pdf-plumber-tool.
2. Create .venv there.
3. Activate it (VS Code usually does this automatically when you select the interpreter).
4. Install packages: pip install pdfplumber pandas.
5. Save dependencies: pip freeze > requirements.txt.
6. Write your code in extract\_pdf.py.

**Copy**

PS C:\Users\David Miley\GitRepos\pdf-plumber-tool> python -m venv .venv Traceback (most recent call last): File "<frozen runpy>", line 198, in \_run\_module\_as\_main File "<frozen runpy>", line 88, in \_run\_code File "C:\Python314\Lib\venv\\_\_main\_\_.py", line 6, in <module> main() ~~~~^^ File "C:\Python314\Lib\venv\\_\_init\_\_.py", line 690, in main builder.create(d) ~~~~~~~~~~~~~~^^^ File "C:\Python314\Lib\venv\\_\_init\_\_.py", line 82, in create self.\_setup\_pip(context) ~~~~~~~~~~~~~~~^^^^^^^^^ File "C:\Python314\Lib\venv\\_\_init\_\_.py", line 458, in \_setup\_pip self.\_call\_new\_python(context, '-m', 'ensurepip', '--upgrade', ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ '--default-pip', stderr=subprocess.STDOUT) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ File "C:\Python314\Lib\venv\\_\_init\_\_.py", line 454, in \_call\_new\_python subprocess.check\_output(args, \*\*kwargs) ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^ File "C:\Python314\Lib\subprocess.py", line 472, in check\_output return run(\*popenargs, stdout=PIPE, timeout=timeout, check=True, ~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ \*\*kwargs).stdout ^^^^^^^^^ File "C:\Python314\Lib\subprocess.py", line 556, in run stdout, stderr = process.communicate(input, timeout=timeout) ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^ File "C:\Python314\Lib\subprocess.py", line 1207, in communicate stdout = self.stdout.read() KeyboardInterrupt PS C:\Users\David Miley\GitRepos\pdf-plumber-tool>

Finished

The error KeyboardInterrupt during ensurepip indicates that the process hung while trying to install pip inside the new virtual environment. This is a **known bug in Python 3.14 on Windows** (specifically with the Microsoft Store version or certain builds) where the ensurepip module freezes.

You can bypass this immediately by creating the environment **without pip**, then installing pip manually.

# 14 Step 1: Create the Virtual Environment Without Pip

Run this command in your VS Code terminal inside C:\Users\David Miley\GitRepos\pdf-plumber-tool:

python -m venv .venv --without-pip

*The --without-pip flag skips the hanging step. The folder will be created successfully.*

# 15 Step 2: Manually Install Pip

Once the .venv folder exists, you need to bootstrap pip into it.

1. Activate the environment (VS Code might do this automatically, but to be safe):

.\.venv\Scripts\Activate.ps1

*(If you get a security error, run Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser first).*

2. Download and run the get-pip script: Run this single command to download the official installer and pipe it directly into your new environment:

curl https://bootstrap.pypa.io/get-pip.py | python

*(Note: If curl is not recognized, use Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py then python get-pip.py)*.

# 16 Step 3: Install Your Dependencies

Now that pip is working, install the libraries you need:

pip install pdfplumber pandas

# 17 Step 4: Verify in VS Code

- Press Ctrl+Shift+P > Python: Select Interpreter.
- Ensure the interpreter pointing to ./.venv/Scripts/python.exe is selected.
- You can now run your script.

[python -m venv --without-pip install pip manually windows](https://search.brave.com/search?q=python%20-m%20venv%20--without-pip%20install%20pip%20manually%20windows)

**View all**

**Copy**

I see a .venv folder so it appears it was created. It has Include, Lib, Scripts folders and .gitignore and pyview.cfg files in it

Finished

The presence of the Include, Lib, and Scripts folders confirms the virtual environment was created successfully. However, because you used --without-pip (or the process hung before finishing), the Scripts folder is likely missing pip.exe.

You need to manually install pip to proceed.

# 18 1. Activate the Environment

Run this in your VS Code terminal:

.\.venv\Scripts\Activate.ps1

*(If blocked by security, run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser)*

You should see (.venv) appear at the start of your command line.

# 19 2. Install Pip Manually

Since pip is missing, download the official installer script and run it with your active environment's Python:

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python get-pip.py

*(If curl fails, use: Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py)*

# 20 3. Verify and Install Libraries

Check that pip is now working:

pip --version

If it returns a version number, install your required packages:

pip install pdfplumber pandas

You can now delete the temporary get-pip.py file and run your script.

**Copy**

I did not run the --without-pip yet

Finished

Since you haven't run the command with --without-pip yet and the folder currently exists in a broken/hung state, you should **delete the existing .venv folder** and start fresh with the workaround.

The error confirms a known issue with **Python 3.14** on Windows where ensurepip hangs indefinitely.

# 21 Step-by-Step Fix in VS Code
1. Delete the Broken Folder In your VS Code terminal (Ctrl+ `), run:

Remove-Item -Recurse -Force .venv

*(Or simply delete the .venv folder manually in the file explorer).*

2. Create Environment Without Pip Run this command to skip the hanging step:

python -m venv .venv --without-pip

*This should complete instantly.*

3. Activate the Environment

.\.venv\Scripts\Activate.ps1

*(If you get an execution policy error, run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser)*.

4. Manually Install Pip Since we skipped the automatic installation, bootstrap it now:
5. curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python get-pip.py

*(If curl fails, use: Invoke-WebRequest -Uri https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py)*.

6. Install Your Libraries Now that pip is working:

pip install pdfplumber pandas

7. Cleanup You can now delete the temporary installer:

Remove-Item get-pip.py

Your environment is now ready. VS Code should automatically detect the new interpreter at .venv\Scripts\python.exe.

**Copy**

pick up where we left off: 3. Critical Step: Ignore the Environment in Git

Finished

Since your .venv folder was created with the --without-pip flag (or failed during creation), it currently lacks a .gitignore file inside it, which newer Python versions usually generate automatically to self-ignore. You must manually create the ignore rule in your **project root**.

# 22 1. Create or Edit the Project .gitignore

In the root of your repository (C:\Users\David Miley\GitRepos\pdf-plumber-tool), create a file named .gitignore if it doesn't exist.

Add the following line to ensure the entire virtual environment folder is ignored:

.venv/

*Note: The trailing slash / is crucial; it tells Git to ignore the****directory****and all its contents, not just a file named .venv.*

# 23 2. Verify the Ignore Rule

To confirm Git is now ignoring the folder, run this command in your terminal:

git status

The .venv folder should **not** appear in the list of "Untracked files".  If it still appears, you may have accidentally added it previously.

# 24 3. Remove Accidentally Tracked Files (If Necessary)

If .venv shows up as "new file to be committed" or was committed in a previous step, untrack it immediately without deleting the actual folder:

git rm -r --cached .venv

git commit -m "Stop tracking virtual environment"

*The --cached flag removes it from Git's index but keeps the files on your hard drive.*

# 25 4. Commit the .gitignore

Finally, commit the .gitignore file itself so this rule applies to everyone who clones your repo:

git add .gitignore

git commit -m "Add .gitignore to exclude virtual environment"

# 26 Recommended Project Structure

Your final folder structure in pdf-plumber-tool should look like this:

pdf-plumber-tool/

├── .git/

├── .venv/ <-- Ignored by Git (contains Scripts, Lib, etc.)

├── .gitignore <-- Contains ".venv/"

├── extract\_pdf.py <-- Your code (Tracked)

└── requirements.txt <-- Dependencies list (Tracked)

[python .gitignore .venv folder best practices](https://search.brave.com/search?q=python%20.gitignore%20.venv%20folder%20best%20practices)

**View all**

**Copy**

(.venv) PS C:\Users\David Miley\GitRepos\pdf-plumber-tool> git status fatal: not a git repository (or any of the parent directories): .git

Finished

The error fatal: not a git repository means you haven't initialized Git in this folder yet. The .git directory mentioned in the previous step doesn't exist.

Run these commands in your VS Code terminal to initialize the repository and set up the ignore rule:

# 27 1. Initialize the Repository

git init

*This creates the hidden .git folder, turning your directory into a repository.*

# 28 2. Create the .gitignore File

Since the folder is new, you likely don't have a .gitignore file yet. Create one and add the rule:

echo .venv/ > .gitignore

*(This command creates the file and writes .venv/ into it in one step).*

# 29 3. Verify and Commit

Check that .venv is now ignored:

git status

You should see .gitignore listed as an untracked file, but **not** .venv.

Now commit the setup:

git add .gitignore

git commit -m "Initial commit: Add .gitignore"

You can now safely install your packages (pip install pdfplumber pandas) without worrying about committing the environment files.

**Copy**

what about the .gitignore file that is visible in the .venv folder?

Finished

The .gitignore file you see **inside** the .venv folder is a **safety feature** automatically generated by Python (specifically in Python 3.13+ and some earlier versions via virtualenv).

# 30 What It Does

- Content: It contains a single asterisk: \*.
- Function: This tells Git to ignore everything inside that specific folder while still tracking the folder itself.
- Scope: It only applies to the .venv directory. It does not ignore the .venv folder from the project root.

# 31 Do You Still Need a Root .gitignore?

**Yes.** You should still keep the .gitignore file in your **project root** (C:\Users\David Miley\GitRepos\pdf-plumber-tool\.gitignore) with the entry:

.venv/

**Why both?**

1. Redundancy: The internal file protects you if you forget the root one.
2. Directory Visibility: The root .gitignore prevents the .venv folder itself from appearing as an "Untracked directory" in git status, keeping your output clean.
3. Best Practice: Standard Python projects always list .venv/ in the root ignore file to ensure consistency across teams and tools.
# 32 Summary

- Keep the file inside .venv (do not delete it).
- Keep your root .gitignore with .venv/ listed.
- Do not commit either the .venv folder or its internal files to Git.  The internal .gitignore ensures that even if you accidentally run git add ., the heavy library files inside .venv won't be staged.