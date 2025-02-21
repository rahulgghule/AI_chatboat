# If using GitHub, clone the repository and navigate into it  
git clone https://github.com/rahulgghule/AI_chatboat.git && cd AI_chatboat  

# Verify remote repository  
git remote -v  

# If not using GitHub, manually create a folder and navigate to it  
mkdir AI_chatboat && cd AI_chatboat  

# Ensure Python and pip are installed  
python --version  
pip --version  

# Create a virtual environment  
python -m venv venv  

# Activate the virtual environment  
# For Windows (CMD or PowerShell)  
venv\Scripts\activate  

# For macOS/Linux  
source venv/bin/activate  

# Verify virtual environment is active  
where python  # Windows  
which python  # macOS/Linux  

# Install dependencies  
pip install --upgrade pip  
pip install -r requirements.txt  

# Ensure requirements.txt exists before running the install command  
if not exist requirements.txt (echo "Error: requirements.txt not found." & exit /b)  

# Run the chatbot  
python -m streamlit run main.py  

# After making changes to the code, update the repository  
git add .  
git commit -m "Your commit message"  
git push origin main  

# Deactivate virtual environment when done  
deactivate  
