# Exam IDE - coding platform - Database Models
Link: https://app.eraser.io/workspace/pXYN2sBX93j66ccyIk9I
## 1️⃣ User Model

```javascript
// models/User.js
{
  // Authentication
  email: String (unique, required),
  password: String (hashed, select: false),
  
  // Profile
  firstName: String (required),
  lastName: String,
  usn: String (unique, sparse),  // For students only
  phone: String,
  avatar: String,
  
  // Role & Permissions
  role: Enum ['student', 'teacher', 'admin', 'superadmin'],
  
  // Status
  isVerified: Boolean (default: false),
  isApproved: Boolean (default: true),  // Teachers need approval
  isActive: Boolean (default: true),
  
  // Academic (Students)
  department: Enum ['cs', 'is', 'ec', 'ai', 'ad', 'cv', 'et', 'ee'],
  semester: Number (1-8),
  
  // Password Reset
  passwordResetToken: String,
  passwordResetExpiry: Date,
  
  // Timestamps
  createdAt, updatedAt
}
```

---

## 2️⃣ Exam Model

```javascript
// models/Exam.js
{
  // Basic Info
  name: String (required),
  description: String,
  instructions: String,
  
  // Creator
  createdBy: ObjectId → User (required),
  
  // Target Audience
  departments: [Enum],  // Multiple departments allowed
  semester: Number,
  
  // Question Configuration
  questionType: Enum ['mcq', 'coding', 'mixed'],
  mcqQuestions: [ObjectId → MCQQuestion],
  codingQuestions: [ObjectId → CodingQuestion],
  
  // Scoring
  totalMarks: Number,
  passingMarks: Number,
  negativeMarking: Boolean (default: false),
  negativeMarkValue: Number,
  
  // Scheduling
  scheduledAt: Date,
  endAt: Date,
  duration: Number (minutes),
  
  // Status
  status: Enum ['draft', 'scheduled', 'live', 'completed', 'cancelled'],
  
  // Settings
  settings: {
    shuffleQuestions: Boolean,
    shuffleOptions: Boolean,
    showResults: Boolean,
    allowReview: Boolean,
    autoSubmit: Boolean,
    
    // Proctoring
    proctoring: {
      enabled: Boolean,
      webcam: Boolean,
      tabSwitch: Boolean,
      fullscreen: Boolean,
      copyPaste: Boolean
    }
  },
  
  // Candidates (for invite-only exams)
  isPublic: Boolean (default: true),
  invitedCandidates: [{ usn: String, email: String }],
  
  createdAt, updatedAt
}
```

---

## 3️⃣ MCQQuestion Model (Question Bank)

```javascript
// models/MCQQuestion.js
{
  // Question Content
  question: String (required),
  options: [String] (exactly 4),
  correctAnswer: String (must be one of options),
  explanation: String,  // Show after submission
  
  // Categorization
  category: Enum ['DSA', 'DBMS', 'OS', 'CN', 'OOP', 'SE', 'AI/ML', 'Other'],
  difficulty: Enum ['easy', 'medium', 'hard'],
  tags: [String],
  
  // Scoring
  marks: Number (default: 1),
  
  // Metadata
  createdBy: ObjectId → User,
  isPublic: Boolean,  // Visible in question bank
  usageCount: Number,  // How many exams used this
  
  createdAt, updatedAt
}
```

---

## 4️⃣ CodingQuestion Model (Question Bank)

```javascript
// models/CodingQuestion.js
{
  // Question Content
  title: String (required),
  description: String (required),  // Problem statement (markdown)
  inputFormat: String,
  outputFormat: String,
  constraints: String,
  
  // Examples
  sampleInput: String,
  sampleOutput: String,
  
  // Test Cases
  testCases: [{
    input: String,
    expectedOutput: String,
    isPublic: Boolean,  // Show to student or hidden
    timeout: Number (ms),
    memoryLimit: Number (MB)
  }],
  
  // Starter Code (per language)
  starterCode: [{
    language: String,  // 'javascript', 'python', 'java', 'cpp'
    code: String
  }],
  
  // Categorization
  category: Enum ['Arrays', 'Strings', 'Trees', 'Graphs', 'DP', 'SQL', ...],
  difficulty: Enum ['easy', 'medium', 'hard'],
  tags: [String],
  
  // Scoring
  maxMarks: Number,
  partialMarking: Boolean,  // Give partial marks based on test cases passed
  
  // Metadata
  createdBy: ObjectId → User,
  isPublic: Boolean,
  
  createdAt, updatedAt
}
```

---

## 5️⃣ Submission Model

```javascript
// models/Submission.js
{
  exam: ObjectId → Exam (required),
  student: ObjectId → User (required),
  
  // Timing
  startedAt: Date,
  submittedAt: Date,
  timeSpent: Number (seconds),
  
  // Status
  status: Enum ['in_progress', 'submitted', 'evaluated', 'abandoned'],
  
  // MCQ Answers
  mcqAnswers: [{
    questionId: ObjectId → MCQQuestion,
    selectedOption: String,
    isCorrect: Boolean,
    marksObtained: Number,
    timeTaken: Number (seconds)
  }],
  
  // Coding Answers
  codingAnswers: [{
    questionId: ObjectId → CodingQuestion,
    code: String,
    language: String,
    submittedAt: Date
  }],
  
  // Scores
  mcqScore: Number,
  codingScore: Number,
  totalScore: Number,
  percentage: Number,
  
  // Metadata
  ipAddress: String,
  userAgent: String,
  
  createdAt, updatedAt
}

// Compound unique index: { exam, student }
```

---

## 6️⃣ EvaluationResult Model (Coding Evaluation)

```javascript
// models/EvaluationResult.js
{
  exam: ObjectId → Exam,
  student: ObjectId → User,
  submission: ObjectId → Submission,
  
  // Per Question Results
  questions: [{
    questionId: ObjectId → CodingQuestion,
    title: String,
    
    // Execution Details
    status: Enum ['pending', 'executed', 'error', 'timeout'],
    language: String,
    code: String,
    
    // Test Case Results
    testCasesTotal: Number,
    testCasesPassed: Number,
    testCases: [{
      input: String,
      expectedOutput: String,
      actualOutput: String,
      passed: Boolean,
      executionTime: Number (ms),
      memoryUsage: Number (KB),
      error: String
    }],
    
    // Score
    score: Number,
    maxScore: Number
  }],
  
  // Summary
  totalScore: Number,
  maxPossibleScore: Number,
  percentage: Number,
  
  evaluatedAt: Date,
  createdAt, updatedAt
}
```

---

## 7️⃣ Integrity Model (Proctoring)

```javascript
// models/Integrity.js
{
  exam: ObjectId → Exam,
  student: ObjectId → User,
  
  // Violation Counts
  tabSwitches: Number (default: 0),
  fullscreenExits: Number (default: 0),
  copyAttempts: Number (default: 0),
  pasteAttempts: Number (default: 0),
  rightClickAttempts: Number (default: 0),
  focusLost: Number (default: 0),
  
  // Webcam Snapshots (if enabled)
  snapshots: [{
    url: String,
    timestamp: Date,
    flagged: Boolean  // AI detected suspicious activity
  }],
  
  // Risk Assessment
  riskScore: Number (0-100),
  riskLevel: Enum ['low', 'medium', 'high', 'critical'],
  
  // Events Log
  events: [{
    type: String,
    timestamp: Date,
    details: Object
  }],
  
  createdAt, updatedAt
}
```

---

## 8️⃣ ActiveSession Model (Exam Sessions)

```javascript
// models/ActiveSession.js
{
  exam: ObjectId → Exam,
  student: ObjectId → User,
  
  // Session State
  status: Enum ['active', 'paused', 'disconnected', 'completed'],
  
  // Timing
  startedAt: Date,
  lastPingAt: Date,
  expiresAt: Date,
  
  // Current Progress
  currentQuestionIndex: Number,
  answeredQuestions: [ObjectId],
  
  // Connection Info
  socketId: String,
  ipAddress: String,
  userAgent: String,
  
  createdAt, updatedAt
}

// TTL index: expires after exam ends
```
