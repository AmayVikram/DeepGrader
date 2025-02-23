# DeepGrader - AI-Powered Assignment Grading

## Website Link

[DeepGrader](https://deepgrader.onrender.com)

## Team Name

**Deep Thinkers**

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/AmayVikram/DeepGrader
cd DeepGrader
```

### 2. Install MongoDB and Set It Up

- Download MongoDB from [MongoDB Official Site](https://www.mongodb.com/try/download/community)
- Install and run the MongoDB service.
- Ensure MongoDB is running before launching the project.

### 3. Set Up the `.env` File

Create a `.env` file in the project root and add the following environment variables:

```env
MONGO_URL=<your-mongodb-connection-string>
MIRA_SDK_API_KEY=<your-mira-sdk-api-key>
```

- Replace `<your-mongodb-connection-string>` with your actual MongoDB connection string.
- Replace `<your-mira-sdk-api-key>` with your API key for Mira SDK.

## How the Website Works

### **User Roles**

- **Teacher**
- **Student**

### **Teacher Flow**

1. **Sign Up as a Teacher** - Upon signing up, a classroom is created along with a unique classroom code.
2. **Add Assignments** - Each assignment consists of multiple questions where:
   - Each question has assigned marks.
   - A model answer is provided for AI grading.
3. **Share Classroom Code** - Students can use this code to join the classroom.

### **Student Flow**

1. **Sign Up as a Student** - Students must enter a classroom code to join.
2. **Submit Assignment Answers** - Assignments are graded by AI instantly upon submission.
3. **View Results & Analysis** -
   - Marks are displayed immediately.
   - A detailed grading analysis is available for each question.

### **File Format Requirement**

- Teachers and students must upload assignments in a prescribed format to ensure smooth processing.

---

DeepGrader ensures quick, automated, and fair assignment grading using AI, providing instant feedback to students and reducing the workload for teachers!

