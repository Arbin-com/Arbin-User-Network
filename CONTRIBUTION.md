# Contributing to Arbin User Network

Thank you for your interest in contributing to the Arbin User Network! This community repository is built for scientists, engineers, and researchers who are using Arbin products and API to share their knowledge, testing protocols, and experience.

## How to Contribute

1. Fork the Repository
Start by forking this repository to your own GitHub account. This allows you to make changes to your copy without affecting the main repository.

2. Create a Branch
Create a new branch for your contribution. Use a descriptive branch name such as:
    ```bash
    git checkout -b add-cccv-schedule
    ```
3. Make Your Changes
Make your contributions in the appropriate folder. See the folder structure and guidelines below for more details.

4. Submit a Pull Request
Once your changes are complete, submit a pull request. We will review it and provide feedback if needed. Please ensure your contribution adheres to the guidelines in this document before submitting.

<details>
    <summary><b>Detailed guide if you're not familiar with Git and GitHub</b></summary>
Don't worry! This guide will walk you through the steps to contribute, including how to use Git for collaboration.

### 1. Set Up Git and GitHub
**Install Git**\
First, you'll need to install Git on your computer. Git is a tool that helps you track changes to your code and collaborate with others.

* Windows: Download and install Git from [here](https://git-scm.com/downloads/win).
* macOS: Install Git by running the following command in your terminal:
    ```bash
    xcode-select --install
    ```
* Linux: Use your package manager to install Git. For example, on Ubuntu, run:
    ```
    sudo apt-get install git
    ```
**Create a GitHub Account**\
If you don’t have a GitHub account yet, sign up at GitHub. It’s free!

### 2. Fork the Repository
A "fork" is your own copy of the repository. This allows you to make changes without affecting the original repository until you're ready to share them.

1. Go to the main repository page: [ARBIN-USER-NETWORK](https://github.com/Arbin-com/Arbin-User-Network).
2. Click the **Fork** button in the upper-right corner of the page. This will create a copy of the repository under your GitHub account.
## 3. Clone Your Fork
Cloning your fork means downloading it to your local machine so you can work on it.
1. Open a terminal or command prompt on your computer.
2. Use the following command to clone your fork of the repository to your local machine:
    ```bash
    git clone https://github.com/Arbin-com/Arbin-User-Network.git
    ```
3. Navigate into the project folder:
    ```bash
    cd ARBIN-USER-NETWORK
    ```
### 4. Create a New Branch
Before you start working on your changes, create a new branch. This keeps your work separate from the `main` branch, so you can make changes without affecting the stable version of the project.

Run this command to create and switch to a new branch:

```bash
git checkout -b [branch-name]
```
Replace `[branch-name]` with something descriptive, such as add-api-example or fix-documentation.

### 5. Make Your Changes
Now you can make changes to the project! Add your files, make edits, or create new documentation as necessary.

Follow the structure provided below based on what you are contributing (API implementation, testing schedules, or tips).

### 6. Stage and Commit Your Changes
Once you’ve made your changes, you need to "stage" and "commit" them. Staging means marking the changes you want to include in the next commit, and committing means saving those changes in your branch.

**Stage Changes**\
Run the following command to stage all your changes:
```bash
git add .
```
**Commit Changes**\
Once the changes are staged, commit them with a message describing what you did:
```bash
git commit -m "Added example API usage script"
```
### 7. Push Your Changes to GitHub
Now that your changes are committed, push them to your GitHub fork:

```bash
git push origin [branch-name]
```
Replace `[branch-name]` with the name of the branch you created earlier.

### 8. Submit a Pull Request
A Pull Request (PR) is how you submit your changes back to the original repository. To do this:

1. Go to the [ARBIN-USER-NETWORK](https://github.com/Arbin-com/Arbin-User-Network.git) repository in your browser.

2. You should see a banner suggesting your new branch. Click the Compare & pull request button.

3. In the pull request description, explain:
    * What your contribution is.
    * What changes you made and why.
    * Any additional information that may be useful for reviewers.
4. Submit the pull request! One of the repository maintainers will review it and, if everything looks good, your changes will be merged.

</details>

## Folder Structure and Guidelines
Make sure to organize your contributions into the correct folder:
```
| ARBIN-USER-NETWORK/
| --- API_Implementations/
| --- | ArbinCTI
| --- | ArbinWebAPI
| --- Testing_Schedules/
| --- Tips_and_Tricks/
```
* `API_Implementations`: For submitting code that interacts with Arbin's API.
* `Testing_Schedules`: For sharing battery testing schedules.
* `Tips_and_Tricks`: For general insights, performance tips, and workflow optimizations.

Within these folders, create a new sub-folder named appropriately for your contribution. For example:


```
| ARBIN-USER-NETWORK/
| --- Testing_Schedules/
|     | --- Direct_Current_Impedance/
|         | --- README.md
|         | --- dcim.sdx
```
Each contribution should include a README.md file explaining:
* The purpose of the contribution.
* Any dependencies or setup steps.
* How to use the files you've provided.

## Contribution Guidelines
* **Code**: Ensure your code is well-commented.
* **Documentation**: Write clear and concise descriptions for your contributions in README.md files.
* **Testing Schedules**: Include details such as the type of batteries used, the goals of the test, and the expected outcomes.


## Need Help?
If you're having trouble with any of the steps or have questions about Git, feel free to ask for help by opening an issue in the repository or participating in discussions.


## Thank You for Contributing!
We’re excited to have you as part of the Arbin User Network. Your contributions help the entire community improve their use of Arbin's products and make advancements in battery testing research.



