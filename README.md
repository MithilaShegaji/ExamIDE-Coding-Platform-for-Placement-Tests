# 🏗️ Exam IDE - coding platform - Complete Architecture Design

> A comprehensive guide to the database models, API endpoints, middleware, and frontend architecture.

---

## 📑 Table of Contents

1. [System Overview](#system-overview)
2. [Database Models](#database-models)
3. [API Endpoints](#api-endpoints)
4. [Middleware](#middleware)
5. [Frontend Architecture](#frontend-architecture)
6. [Folder Structure](#folder-structure)
7. [TanStack Query Setup](#tanstack-query-setup)
8. [Implementation Roadmap](#implementation-roadmap)

---

## System Overview

### Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 19 + Vite + TailwindCSS |
| **Backend** | Express.js (Node.js) |
| **Database** | MongoDB + Mongoose |
| **Auth** | JWT (JSON Web Tokens) |
| **State Management** | TanStack Query (React Query) |
| **Code Execution** | Judge0 API |
| **File Storage** | AWS S3 |
| **Package Manager** | Bun |

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              CLIENT                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    React Frontend (Vite)                         │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │   │
│  │  │  Pages   │  │Components│  │  Hooks   │  │ TanStack Query   │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTP/REST API
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                              SERVER                                      │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    Express.js Backend                            │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │   │
│  │  │  Routes  │  │Controllers│ │ Services │  │   Middleware     │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
            │   MongoDB    │ │   Judge0     │ │    AWS S3    │
            │   (Atlas)    │ │   (Code Exec)│ │  (Storage)   │
            └──────────────┘ └──────────────┘ └──────────────┘
```

---

## Database Models

### Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATABASE SCHEMA                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐     ┌──────────┐     ┌──────────────┐                │
│  │   User   │────▶│   Exam   │────▶│  Submission  │                │
│  └──────────┘     └──────────┘     └──────────────┘                │
│       │                │                   │                        │
│       │                │                   ▼                        │
│       │                │           ┌──────────────┐                │
│       │                │           │  Evaluation  │                │
│       │                │           │    Result    │                │
│       │                │           └──────────────┘                │
│       │                │                                           │
│       │                ├────────▶ ┌──────────────┐                 │
│       │                │          │  MCQQuestion │                 │
│       │                │          └──────────────┘                 │
│       │                │                                           │
│       │                └────────▶ ┌──────────────┐                 │
│       │                           │CodingQuestion│                 │
│       │                           └──────────────┘                 │
│       │                                                            │
│       └─────────────────────────▶ ┌──────────────┐                 │
│                                   │  Integrity   │                 │
│                                   └──────────────┘                 │
│                                                                     │
│       ┌──────────────┐                                             │
│       │ActiveSession │ (Real-time exam tracking)                   │
│       └──────────────┘                                             │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 1️⃣ User Model

**File:** `models/User.js`

```javascript
const userSchema = new mongoose.Schema({
  // ═══════════════════════════════════════════════════════════════
  // AUTHENTICATION
  // ═══════════════════════════════════════════════════════════════
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    trim: true,
    match: [/^\S+@\S+\.\S+$/, 'Please enter a valid email']
  },
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: [6, 'Password must be at least 6 characters'],
    select: false  // Never return password in queries
  },

  // ═══════════════════════════════════════════════════════════════
  // PROFILE INFORMATION
  // ═══════════════════════════════════════════════════════════════
  firstName: {
    type: String,
    required: [true, 'First name is required'],
    trim: true,
    maxlength: [50, 'First name cannot exceed 50 characters']
  },
  lastName: {
    type: String,
    trim: true,
    maxlength: [50, 'Last name cannot exceed 50 characters']
  },
  usn: {
    type: String,
    unique: true,
    sparse: true,  // Allows null values while maintaining uniqueness
    uppercase: true,
    trim: true
  },
  phone: {
    type: String,
    trim: true
  },
  avatar: {
    type: String,
    default: 'https://cdn-icons-png.flaticon.com/128/456/456212.png'
  },

  // ═══════════════════════════════════════════════════════════════
  // ROLE & PERMISSIONS
  // ═══════════════════════════════════════════════════════════════
  role: {
    type: String,
    enum: ['student', 'teacher', 'admin', 'superadmin'],
    default: 'student'
  },

  // ═══════════════════════════════════════════════════════════════
  // STATUS FLAGS
  // ═══════════════════════════════════════════════════════════════
  isVerified: {
    type: Boolean,
    default: false  // Email verification status
  },
  isApproved: {
    type: Boolean,
    default: true   // Teachers need manual approval (set to false)
  },
  isActive: {
    type: Boolean,
    default: true   // Account active/deactivated
  },

  // ═══════════════════════════════════════════════════════════════
  // ACADEMIC INFORMATION (For Students)
  // ═══════════════════════════════════════════════════════════════
  department: {
    type: String,
    enum: ['ad', 'is', 'cs', 'et', 'ec', 'ai', 'cv', 'ee']
  },
  semester: {
    type: Number,
    min: 1,
    max: 8
  },
  year: {
    type: String
  },

  // ═══════════════════════════════════════════════════════════════
  // PASSWORD RESET
  // ═══════════════════════════════════════════════════════════════
  passwordResetToken: String,
  passwordResetExpiry: Date,

  // ═══════════════════════════════════════════════════════════════
  // EMAIL VERIFICATION
  // ═══════════════════════════════════════════════════════════════
  verificationToken: String,
  verificationExpiry: Date

}, { 
  timestamps: true  // Adds createdAt and updatedAt
});

// ═══════════════════════════════════════════════════════════════
// INDEXES
// ═══════════════════════════════════════════════════════════════
userSchema.index({ role: 1 });
userSchema.index({ department: 1, semester: 1 });

// ═══════════════════════════════════════════════════════════════
// VIRTUAL FIELDS
// ═══════════════════════════════════════════════════════════════
userSchema.virtual('fullName').get(function() {
  return `${this.firstName} ${this.lastName || ''}`.trim();
});

// ═══════════════════════════════════════════════════════════════
// INSTANCE METHODS
// ═══════════════════════════════════════════════════════════════
// - comparePassword(candidatePassword)
// - generatePasswordResetToken()
// - generateVerificationToken()
```

**Indexes:**
- `email` - Unique index (from schema)
- `usn` - Unique sparse index (from schema)
- `role` - For filtering by role
- `{ department, semester }` - Compound index for student filtering

---

### 2️⃣ Exam Model

**File:** `models/Exam.js`

```javascript
const examSchema = new mongoose.Schema({
  // ═══════════════════════════════════════════════════════════════
  // BASIC INFORMATION
  // ═══════════════════════════════════════════════════════════════
  name: {
    type: String,
    required: [true, 'Exam name is required'],
    trim: true,
    maxlength: [200, 'Exam name cannot exceed 200 characters']
  },
  description: {
    type: String,
    maxlength: [2000, 'Description cannot exceed 2000 characters']
  },
  instructions: {
    type: String,
    maxlength: [5000, 'Instructions cannot exceed 5000 characters']
  },

  // ═══════════════════════════════════════════════════════════════
  // CREATOR
  // ═══════════════════════════════════════════════════════════════
  createdBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },

  // ═══════════════════════════════════════════════════════════════
  // TARGET AUDIENCE
  // ═══════════════════════════════════════════════════════════════
  departments: [{
    type: String,
    enum: ['ad', 'is', 'cs', 'et', 'ec', 'ai', 'cv', 'ee']
  }],
  semester: {
    type: Number,
    min: 1,
    max: 8
  },

  // ═══════════════════════════════════════════════════════════════
  // QUESTION CONFIGURATION
  // ═══════════════════════════════════════════════════════════════
  questionType: {
    type: String,
    enum: ['mcq', 'coding', 'mixed'],
    required: true
  },
  mcqQuestions: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'MCQQuestion'
  }],
  codingQuestions: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'CodingQuestion'
  }],

  // ═══════════════════════════════════════════════════════════════
  // SCORING
  // ═══════════════════════════════════════════════════════════════
  totalMarks: {
    type: Number,
    default: 0
  },
  passingMarks: {
    type: Number,
    default: 0
  },
  negativeMarking: {
    type: Boolean,
    default: false
  },
  negativeMarkValue: {
    type: Number,
    default: 0
  },

  // ═══════════════════════════════════════════════════════════════
  // SCHEDULING
  // ═══════════════════════════════════════════════════════════════
  scheduledAt: {
    type: Date
  },
  endAt: {
    type: Date
  },
  duration: {
    type: Number,  // In minutes
    required: true
  },

  // ═══════════════════════════════════════════════════════════════
  // STATUS
  // ═══════════════════════════════════════════════════════════════
  status: {
    type: String,
    enum: ['draft', 'scheduled', 'live', 'completed', 'cancelled'],
    default: 'draft'
  },

  // ═══════════════════════════════════════════════════════════════
  // SETTINGS
  // ═══════════════════════════════════════════════════════════════
  settings: {
    shuffleQuestions: { type: Boolean, default: false },
    shuffleOptions: { type: Boolean, default: false },
    showResults: { type: Boolean, default: false },
    allowReview: { type: Boolean, default: false },
    autoSubmit: { type: Boolean, default: true },
    
    // Proctoring Settings
    proctoring: {
      enabled: { type: Boolean, default: false },
      webcam: { type: Boolean, default: false },
      tabSwitch: { type: Boolean, default: true },
      fullscreen: { type: Boolean, default: true },
      copyPaste: { type: Boolean, default: true }
    }
  },

  // ═══════════════════════════════════════════════════════════════
  // ACCESS CONTROL
  // ═══════════════════════════════════════════════════════════════
  isPublic: {
    type: Boolean,
    default: true  // If false, only invited candidates can take
  },
  invitedCandidates: [{
    usn: String,
    email: String,
    invitedAt: { type: Date, default: Date.now }
  }]

}, { timestamps: true });

// ═══════════════════════════════════════════════════════════════
// INDEXES
// ═══════════════════════════════════════════════════════════════
examSchema.index({ createdBy: 1 });
examSchema.index({ status: 1 });
examSchema.index({ scheduledAt: 1 });
examSchema.index({ departments: 1, semester: 1 });

// ═══════════════════════════════════════════════════════════════
// VIRTUAL FIELDS
// ═══════════════════════════════════════════════════════════════
examSchema.virtual('totalQuestions').get(function() {
  return (this.mcqQuestions?.length || 0) + (this.codingQuestions?.length || 0);
});

examSchema.virtual('isLive').get(function() {
  const now = new Date();
  return this.status === 'live' || 
         (this.scheduledAt <= now && this.endAt >= now);
});
```

**Indexes:**
- `createdBy` - Find exams by teacher
- `status` - Filter by exam status
- `scheduledAt` - Sort by schedule
- `{ departments, semester }` - Find exams for specific students

---

### 3️⃣ MCQQuestion Model (Question Bank)

**File:** `models/MCQQuestion.js`

```javascript
const mcqQuestionSchema = new mongoose.Schema({
  // ═══════════════════════════════════════════════════════════════
  // QUESTION CONTENT
  // ═══════════════════════════════════════════════════════════════
  question: {
    type: String,
    required: [true, 'Question text is required'],
    trim: true
  },
  options: {
    type: [String],
    required: true,
    validate: {
      validator: function(options) {
        return options.length >= 2 && options.length <= 6;
      },
      message: 'Must have between 2 and 6 options'
    }
  },
  correctAnswer: {
    type: String,
    required: [true, 'Correct answer is required'],
    validate: {
      validator: function(answer) {
        return this.options.includes(answer);
      },
      message: 'Correct answer must be one of the options'
    }
  },
  explanation: {
    type: String,
    trim: true  // Shown after submission
  },

  // ═══════════════════════════════════════════════════════════════
  // CATEGORIZATION
  // ═══════════════════════════════════════════════════════════════
  category: {
    type: String,
    enum: [
      'Data Structures',
      'Algorithms',
      'DBMS',
      'Operating Systems',
      'Computer Networks',
      'OOP',
      'Software Engineering',
      'AI/ML',
      'Web Development',
      'Mathematics',
      'Aptitude',
      'Other'
    ]
  },
  difficulty: {
    type: String,
    enum: ['easy', 'medium', 'hard'],
    default: 'easy'
  },
  tags: [{
    type: String,
    trim: true
  }],

  // ═══════════════════════════════════════════════════════════════
  // SCORING
  // ═══════════════════════════════════════════════════════════════
  marks: {
    type: Number,
    default: 1,
    min: 0
  },

  // ═══════════════════════════════════════════════════════════════
  // METADATA
  // ═══════════════════════════════════════════════════════════════
  createdBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  isPublic: {
    type: Boolean,
    default: true  // Visible in shared question bank
  },
  usageCount: {
    type: Number,
    default: 0  // How many exams used this question
  }

}, { timestamps: true });

// ═══════════════════════════════════════════════════════════════
// INDEXES
// ═══════════════════════════════════════════════════════════════
mcqQuestionSchema.index({ createdBy: 1 });
mcqQuestionSchema.index({ category: 1 });
mcqQuestionSchema.index({ difficulty: 1 });
mcqQuestionSchema.index({ tags: 1 });
mcqQuestionSchema.index({ isPublic: 1 });

// Text index for search
mcqQuestionSchema.index({ question: 'text', tags: 'text' });
```

**Indexes:**
- `createdBy` - Find questions by author
- `category` - Filter by category
- `difficulty` - Filter by difficulty
- `tags` - Search by tags
- `isPublic` - Filter public questions
- Text index on `question` and `tags` for full-text search

---

### 4️⃣ CodingQuestion Model (Question Bank)

**File:** `models/CodingQuestion.js`

```javascript
// ═══════════════════════════════════════════════════════════════
// SUB-SCHEMAS
// ═══════════════════════════════════════════════════════════════

const testCaseSchema = new mongoose.Schema({
  input: {
    type: String,
    required: true,
    trim: true
  },
  expectedOutput: {
    type: String,
    required: true,
    trim: true
  },
  isPublic: {
    type: Boolean,
    default: false  // Hidden test cases for evaluation
  },
  timeout: {
    type: Number,
    default: 2000  // Milliseconds
  },
  memoryLimit: {
    type: Number,
    default: 256  // MB
  }
}, { _id: true });

const starterCodeSchema = new mongoose.Schema({
  language: {
    type: String,
    required: true,
    enum: ['javascript', 'python', 'java', 'cpp', 'c', 'go', 'rust']
  },
  code: {
    type: String,
    required: true
  }
}, { _id: true });

// ═══════════════════════════════════════════════════════════════
// MAIN SCHEMA
// ═══════════════════════════════════════════════════════════════

const codingQuestionSchema = new mongoose.Schema({
  // ═══════════════════════════════════════════════════════════════
  // QUESTION CONTENT
  // ═══════════════════════════════════════════════════════════════
  title: {
    type: String,
    required: [true, 'Title is required'],
    trim: true,
    maxlength: [200, 'Title cannot exceed 200 characters']
  },
  description: {
    type: String,
    required: [true, 'Description is required'],
    trim: true  // Problem statement (supports markdown)
  },
  inputFormat: {
    type: String,
    trim: true
  },
  outputFormat: {
    type: String,
    trim: true
  },
  constraints: {
    type: String,
    trim: true
  },

  // ═══════════════════════════════════════════════════════════════
  // EXAMPLES
  // ═══════════════════════════════════════════════════════════════
  sampleInput: {
    type: String,
    trim: true
  },
  sampleOutput: {
    type: String,
    trim: true
  },

  // ═══════════════════════════════════════════════════════════════
  // TEST CASES
  // ═══════════════════════════════════════════════════════════════
  testCases: {
    type: [testCaseSchema],
    required: true,
    validate: {
      validator: function(testCases) {
        return testCases.length > 0;
      },
      message: 'At least one test case is required'
    }
  },

  // ═══════════════════════════════════════════════════════════════
  // STARTER CODE
  // ═══════════════════════════════════════════════════════════════
  starterCode: {
    type: [starterCodeSchema],
    default: []
  },

  // ═══════════════════════════════════════════════════════════════
  // SUPPORTED LANGUAGES
  // ═══════════════════════════════════════════════════════════════
  allowedLanguages: [{
    type: String,
    enum: ['javascript', 'python', 'java', 'cpp', 'c', 'go', 'rust']
  }],

  // ═══════════════════════════════════════════════════════════════
  // CATEGORIZATION
  // ═══════════════════════════════════════════════════════════════
  category: {
    type: String,
    enum: [
      'Arrays',
      'Strings',
      'Linked Lists',
      'Stacks',
      'Queues',
      'Trees',
      'Graphs',
      'Recursion',
      'Dynamic Programming',
      'Sorting',
      'Searching',
      'Hashing',
      'Greedy',
      'Backtracking',
      'Math',
      'Bit Manipulation',
      'Matrix',
      'SQL',
      'Other'
    ]
  },
  difficulty: {
    type: String,
    enum: ['easy', 'medium', 'hard'],
    default: 'easy'
  },
  tags: [{
    type: String,
    trim: true
  }],

  // ═══════════════════════════════════════════════════════════════
  // SCORING
  // ═══════════════════════════════════════════════════════════════
  maxMarks: {
    type: Number,
    required: true,
    min: 1
  },
  partialMarking: {
    type: Boolean,
    default: true  // Give partial marks based on test cases passed
  },

  // ═══════════════════════════════════════════════════════════════
  // METADATA
  // ═══════════════════════════════════════════════════════════════
  createdBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  isPublic: {
    type: Boolean,
    default: true
  },
  usageCount: {
    type: Number,
    default: 0
  }

}, { timestamps: true });

// ═══════════════════════════════════════════════════════════════
// INDEXES
// ═══════════════════════════════════════════════════════════════
codingQuestionSchema.index({ createdBy: 1 });
codingQuestionSchema.index({ category: 1 });
codingQuestionSchema.index({ difficulty: 1 });
codingQuestionSchema.index({ tags: 1 });
codingQuestionSchema.index({ isPublic: 1 });

// Text index for search
codingQuestionSchema.index({ title: 'text', description: 'text', tags: 'text' });

// ═══════════════════════════════════════════════════════════════
// VIRTUAL FIELDS
// ═══════════════════════════════════════════════════════════════
codingQuestionSchema.virtual('publicTestCases').get(function() {
  return this.testCases.filter(tc => tc.isPublic);
});

codingQuestionSchema.virtual('totalTestCases').get(function() {
  return this.testCases.length;
});
```

---

### 5️⃣ Submission Model

**File:** `models/Submission.js`

```javascript
// ═══════════════════════════════════════════════════════════════
// SUB-SCHEMAS
// ═══════════════════════════════════════════════════════════════

const mcqAnswerSchema = new mongoose.Schema({
  questionId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'MCQQuestion',
    required: true
  },
  selectedOption: {
    type: String
  },
  isCorrect: {
    type: Boolean
  },
  marksObtained: {
    type: Number,
    default: 0
  },
  timeTaken: {
    type: Number,  // Seconds spent on this question
    default: 0
  }
}, { _id: false });

const codingAnswerSchema = new mongoose.Schema({
  questionId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'CodingQuestion',
    required: true
  },
  code: {
    type: String
  },
  language: {
    type: String,
    enum: ['javascript', 'python', 'java', 'cpp', 'c', 'go', 'rust']
  },
  submittedAt: {
    type: Date
  }
}, { _id: false });

// ═══════════════════════════════════════════════════════════════
// MAIN SCHEMA
// ═══════════════════════════════════════════════════════════════

const submissionSchema = new mongoose.Schema({
  // ═══════════════════════════════════════════════════════════════
  // REFERENCES
  // ═══════════════════════════════════════════════════════════════
  exam: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Exam',
    required: true
  },
  student: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },

  // ═══════════════════════════════════════════════════════════════
  // TIMING
  // ═══════════════════════════════════════════════════════════════
  startedAt: {
    type: Date,
    required: true
  },
  submittedAt: {
    type: Date
  },
  timeSpent: {
    type: Number,  // Total seconds spent
    default: 0
  },

  // ═══════════════════════════════════════════════════════════════
  // STATUS
  // ═══════════════════════════════════════════════════════════════
  status: {
    type: String,
    enum: ['in_progress', 'submitted', 'evaluated', 'abandoned'],
    default: 'in_progress'
  },

  // ═══════════════════════════════════════════════════════════════
  // ANSWERS
  // ═══════════════════════════════════════════════════════════════
  mcqAnswers: [mcqAnswerSchema],
  codingAnswers: [codingAnswerSchema],

  // ═══════════════════════════════════════════════════════════════
  // SCORES
  // ═══════════════════════════════════════════════════════════════
  mcqScore: {
    type: Number,
    default: 0
  },
  codingScore: {
    type: Number,
    default: 0
  },
  totalScore: {
    type: Number,
    default: 0
  },
  percentage: {
    type: Number,
    default: 0
  },
  rank: {
    type: Number  // Calculated after all submissions
  },

  // ═══════════════════════════════════════════════════════════════
  // CLIENT INFORMATION
  // ═══════════════════════════════════════════════════════════════
  ipAddress: {
    type: String
  },
  userAgent: {
    type: String
  }

}, { timestamps: true });

// ═══════════════════════════════════════════════════════════════
// INDEXES
// ═══════════════════════════════════════════════════════════════
submissionSchema.index({ exam: 1, student: 1 }, { unique: true });
submissionSchema.index({ exam: 1, totalScore: -1 });  // For leaderboard
submissionSchema.index({ student: 1, createdAt: -1 }); // Student history
submissionSchema.index({ exam: 1, status: 1 });

// ═══════════════════════════════════════════════════════════════
// VIRTUAL FIELDS
// ═══════════════════════════════════════════════════════════════
submissionSchema.virtual('isPassed').get(function() {
  return this.percentage >= (this.exam?.passingMarks || 0);
});
```

**Key Index:** `{ exam, student }` - Unique compound index to prevent duplicate submissions.

---

### 6️⃣ EvaluationResult Model (Coding Evaluation)

**File:** `models/EvaluationResult.js`

```javascript
// ═══════════════════════════════════════════════════════════════
// SUB-SCHEMAS
// ═══════════════════════════════════════════════════════════════

const testCaseResultSchema = new mongoose.Schema({
  input: String,
  expectedOutput: String,
  actualOutput: String,
  passed: { type: Boolean, default: false },
  error: String,
  executionTime: Number,  // Milliseconds
  memoryUsage: Number     // KB
}, { _id: false });

const executionDetailsSchema = new mongoose.Schema({
  status: {
    type: String,
    enum: ['pending', 'executed', 'compilation_error', 'runtime_error', 'timeout', 'memory_exceeded'],
    default: 'pending'
  },
  compilationError: String,
  runtimeError: String,
  executionTime: { type: Number, default: 0 },
  memoryUsage: { type: Number, default: 0 }
}, { _id: false });

const questionResultSchema = new mongoose.Schema({
  questionId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'CodingQuestion',
    required: true
  },
  title: String,
  code: String,
  language: String,
  
  // Execution
  executionDetails: executionDetailsSchema,
  
  // Results
  testCasesTotal: { type: Number, default: 0 },
  testCasesPassed: { type: Number, default: 0 },
  testCases: [testCaseResultSchema],
  
  // Score
  score: { type: Number, default: 0 },
  maxScore: { type: Number, default: 0 },
  
  // Status
  status: {
    type: String,
    enum: ['correct', 'partial', 'incorrect', 'not_attempted', 'error'],
    default: 'not_attempted'
  }
}, { _id: false });

const summarySchema = new mongoose.Schema({
  totalQuestions: { type: Number, default: 0 },
  attempted: { type: Number, default: 0 },
  correct: { type: Number, default: 0 },
  partial: { type: Number, default: 0 },
  incorrect: { type: Number, default: 0 },
  totalTestCases: { type: Number, default: 0 },
  passedTestCases: { type: Number, default: 0 }
}, { _id: false });

// ═══════════════════════════════════════════════════════════════
// MAIN SCHEMA
// ═══════════════════════════════════════════════════════════════

const evaluationResultSchema = new mongoose.Schema({
  // References
  exam: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Exam',
    required: true
  },
  student: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  submission: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Submission',
    required: true
  },

  // Student Info (denormalized for reporting)
  studentName: String,
  usn: String,

  // Results
  questions: [questionResultSchema],
  summary: summarySchema,

  // Scores
  totalScore: { type: Number, default: 0 },
  maxPossibleScore: { type: Number, default: 0 },
  percentage: { type: Number, default: 0 },

  // Timestamps
  submittedAt: Date,
  evaluatedAt: { type: Date, default: Date.now }

}, { timestamps: true });

// ═══════════════════════════════════════════════════════════════
// INDEXES
// ═══════════════════════════════════════════════════════════════
evaluationResultSchema.index({ exam: 1, student: 1 }, { unique: true });
evaluationResultSchema.index({ exam: 1, totalScore: -1 });  // Leaderboard
evaluationResultSchema.index({ student: 1, evaluatedAt: -1 });  // History
```

---

### 7️⃣ Integrity Model (Proctoring)

**File:** `models/Integrity.js`

```javascript
const integrityEventSchema = new mongoose.Schema({
  type: {
    type: String,
    enum: [
      'tab_switch',
      'fullscreen_exit',
      'copy_attempt',
      'paste_attempt',
      'right_click',
      'focus_lost',
      'devtools_open',
      'screenshot_attempt',
      'face_not_detected',
      'multiple_faces',
      'suspicious_movement'
    ],
    required: true
  },
  timestamp: {
    type: Date,
    default: Date.now
  },
  details: {
    type: mongoose.Schema.Types.Mixed
  }
}, { _id: false });

const snapshotSchema = new mongoose.Schema({
  url: {
    type: String,
    required: true
  },
  timestamp: {
    type: Date,
    default: Date.now
  },
  flagged: {
    type: Boolean,
    default: false
  },
  flagReason: String
}, { _id: true });

const integritySchema = new mongoose.Schema({
  // References
  exam: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Exam',
    required: true
  },
  student: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },

  // ═══════════════════════════════════════════════════════════════
  // VIOLATION COUNTS
  // ═══════════════════════════════════════════════════════════════
  tabSwitches: { type: Number, default: 0 },
  fullscreenExits: { type: Number, default: 0 },
  copyAttempts: { type: Number, default: 0 },
  pasteAttempts: { type: Number, default: 0 },
  rightClickAttempts: { type: Number, default: 0 },
  focusLost: { type: Number, default: 0 },
  devtoolsOpened: { type: Number, default: 0 },

  // ═══════════════════════════════════════════════════════════════
  // WEBCAM DATA
  // ═══════════════════════════════════════════════════════════════
  snapshots: [snapshotSchema],
  faceDetectionIssues: { type: Number, default: 0 },

  // ═══════════════════════════════════════════════════════════════
  // EVENTS LOG
  // ═══════════════════════════════════════════════════════════════
  events: [integrityEventSchema],

  // ═══════════════════════════════════════════════════════════════
  // RISK ASSESSMENT
  // ═══════════════════════════════════════════════════════════════
  riskScore: {
    type: Number,
    default: 0,
    min: 0,
    max: 100
  },
  riskLevel: {
    type: String,
    enum: ['low', 'medium', 'high', 'critical'],
    default: 'low'
  },

  // ═══════════════════════════════════════════════════════════════
  // SESSION INFO
  // ═══════════════════════════════════════════════════════════════
  screenConfiguration: String,
  browserInfo: String,
  lastEventAt: Date

}, { timestamps: true });

// ═══════════════════════════════════════════════════════════════
// INDEXES
// ═══════════════════════════════════════════════════════════════
integritySchema.index({ exam: 1, student: 1 }, { unique: true });
integritySchema.index({ exam: 1, riskLevel: 1 });

// ═══════════════════════════════════════════════════════════════
// METHODS
// ═══════════════════════════════════════════════════════════════
integritySchema.methods.calculateRiskScore = function() {
  const weights = {
    tabSwitches: 10,
    fullscreenExits: 15,
    copyAttempts: 20,
    pasteAttempts: 20,
    focusLost: 5,
    devtoolsOpened: 25,
    faceDetectionIssues: 15
  };

  let score = 0;
  score += Math.min(this.tabSwitches * weights.tabSwitches, 30);
  score += Math.min(this.fullscreenExits * weights.fullscreenExits, 30);
  score += Math.min(this.copyAttempts * weights.copyAttempts, 20);
  score += Math.min(this.pasteAttempts * weights.pasteAttempts, 20);
  score += Math.min(this.focusLost * weights.focusLost, 15);
  score += Math.min(this.devtoolsOpened * weights.devtoolsOpened, 25);
  score += Math.min(this.faceDetectionIssues * weights.faceDetectionIssues, 30);

  this.riskScore = Math.min(score, 100);
  
  if (this.riskScore <= 20) this.riskLevel = 'low';
  else if (this.riskScore <= 50) this.riskLevel = 'medium';
  else if (this.riskScore <= 75) this.riskLevel = 'high';
  else this.riskLevel = 'critical';

  return this.riskScore;
};
```

---

### 8️⃣ ActiveSession Model (Real-time Tracking)

**File:** `models/ActiveSession.js`

```javascript
const activeSessionSchema = new mongoose.Schema({
  // References
  exam: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Exam',
    required: true
  },
  student: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  submission: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Submission'
  },

  // ═══════════════════════════════════════════════════════════════
  // SESSION STATE
  // ═══════════════════════════════════════════════════════════════
  status: {
    type: String,
    enum: ['active', 'paused', 'disconnected', 'completed', 'terminated'],
    default: 'active'
  },

  // ═══════════════════════════════════════════════════════════════
  // TIMING
  // ═══════════════════════════════════════════════════════════════
  startedAt: {
    type: Date,
    required: true,
    default: Date.now
  },
  lastPingAt: {
    type: Date,
    default: Date.now
  },
  expiresAt: {
    type: Date,
    required: true
  },

  // ═══════════════════════════════════════════════════════════════
  // PROGRESS
  // ═══════════════════════════════════════════════════════════════
  currentQuestionIndex: {
    type: Number,
    default: 0
  },
  answeredQuestions: [{
    type: mongoose.Schema.Types.ObjectId
  }],

  // ═══════════════════════════════════════════════════════════════
  // CONNECTION INFO
  // ═══════════════════════════════════════════════════════════════
  socketId: String,
  ipAddress: String,
  userAgent: String,

  // ═══════════════════════════════════════════════════════════════
  // FLAGS
  // ═══════════════════════════════════════════════════════════════
  isAllowedResubmit: {
    type: Boolean,
    default: false
  }

}, { 
  timestamps: true
});

// ═══════════════════════════════════════════════════════════════
// INDEXES
// ═══════════════════════════════════════════════════════════════
activeSessionSchema.index({ exam: 1, student: 1 }, { unique: true });
activeSessionSchema.index({ status: 1 });
activeSessionSchema.index({ lastPingAt: 1 });
activeSessionSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 0 }); // TTL index

// ═══════════════════════════════════════════════════════════════
// METHODS
// ═══════════════════════════════════════════════════════════════
activeSessionSchema.methods.isExpired = function() {
  return new Date() > this.expiresAt;
};

activeSessionSchema.methods.ping = function() {
  this.lastPingAt = new Date();
  this.status = 'active';
  return this.save();
};

activeSessionSchema.methods.markDisconnected = function() {
  if (this.status === 'active') {
    this.status = 'disconnected';
    return this.save();
  }
};
```

**TTL Index:** `expiresAt` with `expireAfterSeconds: 0` automatically deletes expired sessions.

---

## API Endpoints

### Authentication (`/api/auth`)

| Method | Endpoint | Description | Access | Request Body |
|--------|----------|-------------|--------|--------------|
| `POST` | `/register` | Register new user | Public | `{ email, password, firstName, lastName, role, usn?, department?, semester? }` |
| `POST` | `/login` | Login user | Public | `{ email, password }` |
| `POST` | `/logout` | Logout user | Protected | - |
| `GET` | `/me` | Get current user | Protected | - |
| `PUT` | `/update-profile` | Update profile | Protected | `{ firstName?, lastName?, phone?, avatar? }` |
| `PUT` | `/update-password` | Change password | Protected | `{ currentPassword, newPassword }` |
| `POST` | `/forgot-password` | Request password reset | Public | `{ email }` |
| `PUT` | `/reset-password/:token` | Reset password | Public | `{ password }` |
| `POST` | `/verify-email/:token` | Verify email | Public | - |

---

### Users (`/api/users`)

| Method | Endpoint | Description | Access | Query Params |
|--------|----------|-------------|--------|--------------|
| `GET` | `/` | List all users (paginated) | Admin | `page, limit, role, department, semester, search` |
| `GET` | `/:id` | Get user details | Admin | - |
| `PUT` | `/:id` | Update user | Admin | - |
| `DELETE` | `/:id` | Deactivate user | Admin | - |
| `PUT` | `/:id/approve` | Approve teacher | Admin | - |
| `PUT` | `/:id/reject` | Reject teacher | Admin | - |
| `GET` | `/teachers/pending` | List pending teachers | Admin | - |
| `GET` | `/students` | List students | Teacher+ | `department, semester, search` |

---

### Exams (`/api/exams`)

| Method | Endpoint | Description | Access | Query Params |
|--------|----------|-------------|--------|--------------|
| `GET` | `/` | List exams | Protected | `status, page, limit` |
| `GET` | `/available` | List available exams for student | Student | - |
| `GET` | `/:id` | Get exam details | Protected | - |
| `POST` | `/` | Create new exam | Teacher+ | - |
| `PUT` | `/:id` | Update exam | Owner | - |
| `DELETE` | `/:id` | Delete exam | Owner | - |
| `POST` | `/:id/publish` | Publish exam | Owner | - |
| `POST` | `/:id/cancel` | Cancel exam | Owner | - |
| `POST` | `/:id/duplicate` | Duplicate exam | Owner | - |
| `GET` | `/:id/candidates` | List eligible candidates | Owner | - |
| `POST` | `/:id/invite` | Invite candidates | Owner | `{ candidates: [{ usn, email }] }` |
| `GET` | `/:id/submissions` | List all submissions | Owner | `page, limit` |
| `GET` | `/:id/analytics` | Get exam analytics | Owner | - |
| `GET` | `/:id/leaderboard` | Get leaderboard | Protected | `limit` |
| `POST` | `/:id/export` | Export results (CSV/Excel) | Owner | `format` |

---

### Questions - MCQ (`/api/questions/mcq`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/` | List MCQ questions | Teacher+ |
| `GET` | `/:id` | Get question details | Teacher+ |
| `POST` | `/` | Create question | Teacher+ |
| `PUT` | `/:id` | Update question | Owner |
| `DELETE` | `/:id` | Delete question | Owner |
| `POST` | `/bulk-import` | Import from CSV/JSON | Teacher+ |
| `GET` | `/categories` | List categories | Teacher+ |

**Query Params for GET `/`:**
- `page`, `limit` - Pagination
- `category` - Filter by category
- `difficulty` - Filter by difficulty
- `search` - Text search
- `createdBy` - Filter by author (admin only)

---

### Questions - Coding (`/api/questions/coding`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/` | List coding questions | Teacher+ |
| `GET` | `/:id` | Get question details | Teacher+ |
| `POST` | `/` | Create question | Teacher+ |
| `PUT` | `/:id` | Update question | Owner |
| `DELETE` | `/:id` | Delete question | Owner |
| `POST` | `/:id/test-cases` | Add test cases | Owner |
| `PUT` | `/:id/test-cases/:tcId` | Update test case | Owner |
| `DELETE` | `/:id/test-cases/:tcId` | Delete test case | Owner |
| `GET` | `/categories` | List categories | Teacher+ |

---

### Exam Session (`/api/exam-session`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `POST` | `/:examId/start` | Start exam session | Student |
| `GET` | `/:examId/questions` | Get exam questions | Student (in session) |
| `POST` | `/:examId/answer` | Submit/update answer | Student (in session) |
| `POST` | `/:examId/submit` | Final submission | Student (in session) |
| `GET` | `/:examId/status` | Get current progress | Student (in session) |
| `POST` | `/:examId/ping` | Keep session alive | Student (in session) |
| `GET` | `/:examId/remaining-time` | Get remaining time | Student (in session) |

---

### Code Execution (`/api/execute`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `POST` | `/run` | Run code (returns output) | Student (in session) |
| `POST` | `/submit` | Submit for evaluation | Student (in session) |
| `GET` | `/languages` | List supported languages | Protected |
| `GET` | `/status/:token` | Check execution status | Protected |

**Request Body for `/run`:**
```json
{
  "code": "print('Hello')",
  "language": "python",
  "input": "test input"
}
```

---

### Submissions (`/api/submissions`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/my` | Get my submissions | Student |
| `GET` | `/:id` | Get submission details | Owner/Teacher |
| `GET` | `/:id/report` | Get detailed report | Owner/Teacher |

---

### Integrity/Proctoring (`/api/integrity`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `POST` | `/:examId/event` | Log integrity event | Student (in session) |
| `POST` | `/:examId/snapshot` | Upload webcam snapshot | Student (in session) |
| `GET` | `/:examId/:studentId` | Get integrity report | Teacher+ |
| `GET` | `/:examId/flagged` | List flagged submissions | Teacher+ |

---

### Dashboard (`/api/dashboard`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| `GET` | `/student` | Student dashboard data | Student |
| `GET` | `/teacher` | Teacher dashboard data | Teacher |
| `GET` | `/admin` | Admin dashboard data | Admin |
| `GET` | `/stats` | Platform statistics | Admin |

---

## Middleware

### 1. Authentication Middleware

**File:** `middleware/auth.js`

```javascript
// Verify JWT token and attach user to request
export const protect = async (req, res, next) => {
  // 1. Get token from header or cookie
  // 2. Verify token
  // 3. Find user
  // 4. Attach user to req.user
  // 5. Call next()
};

// Check if user has required role
export const authorize = (...roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return next(new AppError('Not authorized', 403));
    }
    next();
  };
};

// Check if user owns the resource
export const checkOwnership = (model) => {
  return async (req, res, next) => {
    const resource = await model.findById(req.params.id);
    if (!resource) {
      return next(new AppError('Resource not found', 404));
    }
    if (resource.createdBy.toString() !== req.user._id.toString() && 
        !['admin', 'superadmin'].includes(req.user.role)) {
      return next(new AppError('Not authorized', 403));
    }
    req.resource = resource;
    next();
  };
};
```

---

### 2. Error Handler Middleware

**File:** `middleware/errorHandler.js`

```javascript
export class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
  }
}

export const errorHandler = (err, req, res, next) => {
  let statusCode = err.statusCode || 500;
  let message = err.message || 'Internal Server Error';

  // Handle specific error types:
  // - Mongoose ValidationError
  // - Mongoose CastError
  // - Duplicate key error (code 11000)
  // - JWT errors

  res.status(statusCode).json({
    success: false,
    error: message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};

export const notFoundHandler = (req, res) => {
  res.status(404).json({
    success: false,
    error: 'Route not found'
  });
};
```

---

### 3. Validation Middleware

**File:** `middleware/validate.js`

```javascript
import { ZodError } from 'zod';

export const validate = (schema) => {
  return (req, res, next) => {
    try {
      schema.parse({
        body: req.body,
        query: req.query,
        params: req.params
      });
      next();
    } catch (error) {
      if (error instanceof ZodError) {
        const message = error.errors.map(e => 
          `${e.path.join('.')}: ${e.message}`
        ).join(', ');
        return res.status(400).json({
          success: false,
          error: message
        });
      }
      next(error);
    }
  };
};
```

---

### 4. Rate Limiting Middleware

**File:** `middleware/rateLimit.js`

```javascript
import rateLimit from 'express-rate-limit';

// General API rate limit
export const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,
  message: {
    success: false,
    error: 'Too many requests, please try again later'
  }
});

// Stricter limit for auth routes
export const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: {
    success: false,
    error: 'Too many login attempts, please try again later'
  }
});

// Limit for code execution
export const executionLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 20,
  message: {
    success: false,
    error: 'Too many code executions, please wait'
  }
});
```

---

### 5. Exam Session Middleware

**File:** `middleware/examSession.js`

```javascript
import ActiveSession from '../models/ActiveSession.js';
import { AppError } from './errorHandler.js';

// Verify student has active exam session
export const verifyExamSession = async (req, res, next) => {
  const { examId } = req.params;
  const studentId = req.user._id;

  const session = await ActiveSession.findOne({
    exam: examId,
    student: studentId,
    status: 'active'
  });

  if (!session) {
    return next(new AppError('No active exam session found', 403));
  }

  if (session.isExpired()) {
    session.status = 'completed';
    await session.save();
    return next(new AppError('Exam session has expired', 403));
  }

  req.examSession = session;
  next();
};

// Check if exam is currently live
export const checkExamTiming = async (req, res, next) => {
  const exam = req.exam || await Exam.findById(req.params.examId);
  
  if (!exam) {
    return next(new AppError('Exam not found', 404));
  }

  const now = new Date();
  
  if (now < exam.scheduledAt) {
    return next(new AppError('Exam has not started yet', 403));
  }
  
  if (now > exam.endAt) {
    return next(new AppError('Exam has ended', 403));
  }

  req.exam = exam;
  next();
};

// Prevent duplicate submissions
export const preventResubmit = async (req, res, next) => {
  const existing = await Submission.findOne({
    exam: req.params.examId,
    student: req.user._id,
    status: 'submitted'
  });

  if (existing && !req.examSession?.isAllowedResubmit) {
    return next(new AppError('You have already submitted this exam', 403));
  }

  next();
};
```

---

### 6. File Upload Middleware

**File:** `middleware/upload.js`

```javascript
import multer from 'multer';
import path from 'path';
import { AppError } from './errorHandler.js';

// Memory storage for S3 uploads
const storage = multer.memoryStorage();

// File filter
const fileFilter = (allowedTypes) => (req, file, cb) => {
  const ext = path.extname(file.originalname).toLowerCase();
  if (allowedTypes.includes(ext)) {
    cb(null, true);
  } else {
    cb(new AppError(`Only ${allowedTypes.join(', ')} files allowed`, 400), false);
  }
};

// CSV/Excel upload for bulk import
export const uploadCSV = multer({
  storage,
  fileFilter: fileFilter(['.csv', '.xlsx', '.xls']),
  limits: { fileSize: 5 * 1024 * 1024 } // 5MB
}).single('file');

// Image upload for webcam snapshots
export const uploadImage = multer({
  storage,
  fileFilter: fileFilter(['.jpg', '.jpeg', '.png']),
  limits: { fileSize: 2 * 1024 * 1024 } // 2MB
}).single('image');

// Profile avatar upload
export const uploadAvatar = multer({
  storage,
  fileFilter: fileFilter(['.jpg', '.jpeg', '.png', '.gif']),
  limits: { fileSize: 1 * 1024 * 1024 } // 1MB
}).single('avatar');
```

---

## Frontend Architecture

### Component Structure

```
src/
├── components/
│   ├── ui/                 # Atomic UI components
│   │   ├── Button.jsx
│   │   ├── Input.jsx
│   │   ├── Select.jsx
│   │   ├── Card.jsx
│   │   ├── Modal.jsx
│   │   ├── Table.jsx
│   │   ├── Tabs.jsx
│   │   ├── Badge.jsx
│   │   ├── Toast.jsx
│   │   ├── Dropdown.jsx
│   │   ├── Pagination.jsx
│   │   └── index.js
│   │
│   ├── layout/             # Layout components
│   │   ├── Header.jsx
│   │   ├── Sidebar.jsx
│   │   ├── Footer.jsx
│   │   ├── MainLayout.jsx
│   │   └── AuthLayout.jsx
│   │
│   ├── common/             # Shared components
│   │   ├── Loader.jsx
│   │   ├── PageLoader.jsx
│   │   ├── ErrorBoundary.jsx
│   │   ├── ProtectedRoute.jsx
│   │   ├── RoleBasedRoute.jsx
│   │   └── EmptyState.jsx
│   │
│   └── features/           # Feature-specific components
│       ├── exam/
│       │   ├── ExamCard.jsx
│       │   ├── ExamForm.jsx
│       │   ├── ExamTimer.jsx
│       │   ├── QuestionNavigator.jsx
│       │   └── MCQQuestion.jsx
│       │
│       ├── questions/
│       │   ├── MCQForm.jsx
│       │   ├── CodingForm.jsx
│       │   ├── QuestionCard.jsx
│       │   └── CodeEditor.jsx
│       │
│       └── dashboard/
│           ├── StatsCard.jsx
│           ├── RecentExams.jsx
│           └── Leaderboard.jsx
```

---

### Page Structure

```
src/pages/
├── auth/
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── ForgotPassword.jsx
│   └── ResetPassword.jsx
│
├── dashboard/
│   ├── StudentDashboard.jsx
│   ├── TeacherDashboard.jsx
│   └── AdminDashboard.jsx
│
├── exams/
│   ├── ExamsList.jsx
│   ├── ExamCreate.jsx
│   ├── ExamEdit.jsx
│   ├── ExamDetails.jsx
│   ├── ExamTake.jsx           # Student takes exam
│   ├── ExamSubmissions.jsx    # View all submissions
│   └── ExamAnalytics.jsx
│
├── questions/
│   ├── MCQList.jsx
│   ├── MCQCreate.jsx
│   ├── MCQEdit.jsx
│   ├── CodingList.jsx
│   ├── CodingCreate.jsx
│   └── CodingEdit.jsx
│
├── results/
│   ├── MyResults.jsx
│   ├── ResultDetails.jsx
│   └── Leaderboard.jsx
│
├── profile/
│   ├── Profile.jsx
│   └── Settings.jsx
│
└── admin/
    ├── Users.jsx
    ├── PendingApprovals.jsx
    └── SystemStats.jsx
```

---

## TanStack Query Setup

### Installation

```bash
cd apps/frontend
bun add @tanstack/react-query @tanstack/react-query-devtools
```

### Query Client Configuration

**File:** `src/lib/queryClient.js`

```javascript
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,      // Data considered fresh for 5 minutes
      cacheTime: 30 * 60 * 1000,     // Cache kept for 30 minutes
      refetchOnWindowFocus: false,    // Don't refetch on window focus
      retry: 1,                       // Retry failed requests once
      refetchOnMount: true,
    },
    mutations: {
      retry: 0,                       // Don't retry mutations
    },
  },
});
```

### Provider Setup

**File:** `src/App.jsx`

```javascript
import { QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { queryClient } from './lib/queryClient';

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          {/* Routes */}
        </AuthProvider>
      </BrowserRouter>
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}
```

### Query Keys Convention

```javascript
// Query Keys - Organized and predictable
export const queryKeys = {
  // Auth
  auth: {
    me: ['auth', 'me'],
  },
  
  // Users
  users: {
    all: ['users'],
    list: (filters) => ['users', 'list', filters],
    detail: (id) => ['users', 'detail', id],
    pendingTeachers: ['users', 'pending-teachers'],
  },
  
  // Exams
  exams: {
    all: ['exams'],
    list: (filters) => ['exams', 'list', filters],
    detail: (id) => ['exams', 'detail', id],
    submissions: (id) => ['exams', id, 'submissions'],
    analytics: (id) => ['exams', id, 'analytics'],
    leaderboard: (id) => ['exams', id, 'leaderboard'],
    available: ['exams', 'available'],
  },
  
  // Questions
  questions: {
    mcq: {
      all: ['questions', 'mcq'],
      list: (filters) => ['questions', 'mcq', 'list', filters],
      detail: (id) => ['questions', 'mcq', 'detail', id],
    },
    coding: {
      all: ['questions', 'coding'],
      list: (filters) => ['questions', 'coding', 'list', filters],
      detail: (id) => ['questions', 'coding', 'detail', id],
    },
  },
  
  // Submissions
  submissions: {
    my: ['submissions', 'my'],
    detail: (id) => ['submissions', 'detail', id],
  },
  
  // Dashboard
  dashboard: {
    student: ['dashboard', 'student'],
    teacher: ['dashboard', 'teacher'],
    admin: ['dashboard', 'admin'],
  },
};
```

### Example Hooks

**File:** `src/hooks/useExams.js`

```javascript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../services/api';
import { queryKeys } from '../lib/queryKeys';

// ═══════════════════════════════════════════════════════════════
// QUERIES
// ═══════════════════════════════════════════════════════════════

// List exams with filters
export function useExams(filters = {}) {
  return useQuery({
    queryKey: queryKeys.exams.list(filters),
    queryFn: async () => {
      const { data } = await api.get('/exams', { params: filters });
      return data;
    },
  });
}

// Get single exam
export function useExam(id) {
  return useQuery({
    queryKey: queryKeys.exams.detail(id),
    queryFn: async () => {
      const { data } = await api.get(`/exams/${id}`);
      return data;
    },
    enabled: !!id,  // Only run if id exists
  });
}

// Get available exams for student
export function useAvailableExams() {
  return useQuery({
    queryKey: queryKeys.exams.available,
    queryFn: async () => {
      const { data } = await api.get('/exams/available');
      return data;
    },
  });
}

// Get exam leaderboard
export function useExamLeaderboard(examId, limit = 10) {
  return useQuery({
    queryKey: queryKeys.exams.leaderboard(examId),
    queryFn: async () => {
      const { data } = await api.get(`/exams/${examId}/leaderboard`, {
        params: { limit }
      });
      return data;
    },
    enabled: !!examId,
  });
}

// ═══════════════════════════════════════════════════════════════
// MUTATIONS
// ═══════════════════════════════════════════════════════════════

// Create exam
export function useCreateExam() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (examData) => {
      const { data } = await api.post('/exams', examData);
      return data;
    },
    onSuccess: () => {
      // Invalidate and refetch exams list
      queryClient.invalidateQueries({ queryKey: queryKeys.exams.all });
    },
  });
}

// Update exam
export function useUpdateExam() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async ({ id, ...examData }) => {
      const { data } = await api.put(`/exams/${id}`, examData);
      return data;
    },
    onSuccess: (data, variables) => {
      // Update cache for this specific exam
      queryClient.setQueryData(
        queryKeys.exams.detail(variables.id), 
        data
      );
      // Invalidate list
      queryClient.invalidateQueries({ queryKey: queryKeys.exams.all });
    },
  });
}

// Delete exam
export function useDeleteExam() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (id) => {
      await api.delete(`/exams/${id}`);
      return id;
    },
    onSuccess: (deletedId) => {
      // Remove from cache
      queryClient.removeQueries({ 
        queryKey: queryKeys.exams.detail(deletedId) 
      });
      // Invalidate list
      queryClient.invalidateQueries({ queryKey: queryKeys.exams.all });
    },
  });
}

// Publish exam
export function usePublishExam() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (id) => {
      const { data } = await api.post(`/exams/${id}/publish`);
      return data;
    },
    onSuccess: (data, id) => {
      queryClient.setQueryData(queryKeys.exams.detail(id), data);
      queryClient.invalidateQueries({ queryKey: queryKeys.exams.all });
    },
  });
}
```

### Usage in Components

```javascript
// pages/exams/ExamsList.jsx
import { useExams, useDeleteExam } from '../../hooks/useExams';
import { useState } from 'react';
import { Loader, Button, Card } from '../../components/ui';
import { toast } from 'react-hot-toast';

function ExamsList() {
  const [filters, setFilters] = useState({ status: 'all', page: 1 });
  
  // Fetch exams
  const { data, isLoading, isError, error } = useExams(filters);
  
  // Delete mutation
  const deleteExam = useDeleteExam();

  const handleDelete = async (id) => {
    if (confirm('Are you sure?')) {
      try {
        await deleteExam.mutateAsync(id);
        toast.success('Exam deleted successfully');
      } catch (error) {
        toast.error(error.message);
      }
    }
  };

  if (isLoading) return <Loader />;
  if (isError) return <div>Error: {error.message}</div>;

  return (
    <div className="space-y-4">
      {data.exams.map(exam => (
        <Card key={exam._id}>
          <h3>{exam.name}</h3>
          <p>Status: {exam.status}</p>
          <Button 
            variant="danger" 
            onClick={() => handleDelete(exam._id)}
            loading={deleteExam.isPending}
          >
            Delete
          </Button>
        </Card>
      ))}
    </div>
  );
}
```

---

## Folder Structure

### Backend Structure

```
apps/backend/
├── src/
│   ├── config/
│   │   ├── index.js           # Environment variables
│   │   └── database.js        # MongoDB connection
│   │
│   ├── middleware/
│   │   ├── auth.js            # Authentication & authorization
│   │   ├── errorHandler.js    # Global error handling
│   │   ├── validate.js        # Request validation
│   │   ├── rateLimit.js       # Rate limiting
│   │   ├── examSession.js     # Exam session verification
│   │   └── upload.js          # File upload handling
│   │
│   ├── models/
│   │   ├── User.js
│   │   ├── Exam.js
│   │   ├── MCQQuestion.js
│   │   ├── CodingQuestion.js
│   │   ├── Submission.js
│   │   ├── EvaluationResult.js
│   │   ├── Integrity.js
│   │   └── ActiveSession.js
│   │
│   ├── modules/
│   │   ├── auth/
│   │   │   ├── auth.routes.js
│   │   │   ├── auth.controller.js
│   │   │   └── auth.validation.js
│   │   │
│   │   ├── users/
│   │   │   ├── users.routes.js
│   │   │   ├── users.controller.js
│   │   │   └── users.validation.js
│   │   │
│   │   ├── exams/
│   │   │   ├── exams.routes.js
│   │   │   ├── exams.controller.js
│   │   │   └── exams.validation.js
│   │   │
│   │   ├── questions/
│   │   │   ├── mcq/
│   │   │   │   ├── mcq.routes.js
│   │   │   │   ├── mcq.controller.js
│   │   │   │   └── mcq.validation.js
│   │   │   └── coding/
│   │   │       ├── coding.routes.js
│   │   │       ├── coding.controller.js
│   │   │       └── coding.validation.js
│   │   │
│   │   ├── exam-session/
│   │   │   ├── session.routes.js
│   │   │   └── session.controller.js
│   │   │
│   │   ├── execution/
│   │   │   ├── execution.routes.js
│   │   │   └── execution.controller.js
│   │   │
│   │   ├── submissions/
│   │   │   ├── submissions.routes.js
│   │   │   └── submissions.controller.js
│   │   │
│   │   ├── integrity/
│   │   │   ├── integrity.routes.js
│   │   │   └── integrity.controller.js
│   │   │
│   │   └── dashboard/
│   │       ├── dashboard.routes.js
│   │       └── dashboard.controller.js
│   │
│   ├── services/
│   │   ├── email.service.js     # Email sending
│   │   ├── judge0.service.js    # Code execution
│   │   ├── s3.service.js        # File uploads
│   │   └── evaluation.service.js # Code evaluation
│   │
│   ├── utils/
│   │   └── helpers.js           # Utility functions
│   │
│   ├── app.js                   # Express app setup
│   └── index.js                 # Server entry point
│
├── package.json
└── .env
```

### Frontend Structure

```
apps/frontend/
├── src/
│   ├── components/
│   │   ├── ui/                  # Reusable UI components
│   │   ├── layout/              # Layout components
│   │   ├── common/              # Shared components
│   │   └── features/            # Feature-specific components
│   │
│   ├── context/
│   │   └── AuthContext.jsx      # Authentication context
│   │
│   ├── hooks/
│   │   ├── useAuth.js
│   │   ├── useExams.js
│   │   ├── useQuestions.js
│   │   ├── useSubmissions.js
│   │   ├── useUsers.js
│   │   └── useDashboard.js
│   │
│   ├── lib/
│   │   ├── queryClient.js       # TanStack Query client
│   │   └── queryKeys.js         # Query key constants
│   │
│   ├── pages/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── exams/
│   │   ├── questions/
│   │   ├── results/
│   │   ├── profile/
│   │   └── admin/
│   │
│   ├── services/
│   │   └── api.js               # Axios instance
│   │
│   ├── utils/
│   │   ├── helpers.js
│   │   └── constants.js
│   │
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1)
- [x] Project setup (monorepo with Bun)
- [x] Backend Express setup
- [x] Frontend React + Vite setup
- [x] User model & authentication
- [x] Basic UI components
- [ ] TanStack Query setup

### Phase 2: Core Features (Week 2-3)
- [ ] All database models
- [ ] MCQ Question module (CRUD)
- [ ] Coding Question module (CRUD)
- [ ] Exam module (CRUD)
- [ ] Question bank UI

### Phase 3: Exam Taking (Week 4)
- [ ] Exam session management
- [ ] MCQ taking interface
- [ ] Code editor integration
- [ ] Judge0 integration
- [ ] Auto-submit on timeout

### Phase 4: Results & Analytics (Week 5)
- [ ] Submission processing
- [ ] Code evaluation
- [ ] Results display
- [ ] Leaderboard
- [ ] Export functionality

### Phase 5: Proctoring & Admin (Week 6)
- [ ] Integrity monitoring
- [ ] Webcam snapshots
- [ ] Admin dashboard
- [ ] User management
- [ ] Teacher approval flow

### Phase 6: Polish (Week 7)
- [ ] UI/UX improvements
- [ ] Performance optimization
- [ ] Testing
- [ ] Documentation
- [ ] Deployment

---

## Environment Variables

### Backend (.env)

```env
# Server
PORT=5000
NODE_ENV=development

# Database
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/prepzero_v2

# JWT
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRES_IN=7d

# Frontend URL (CORS)
FRONTEND_URL=http://localhost:5173

# Judge0 API
JUDGE0_API_URL=http://localhost:2358
JUDGE0_API_KEY=

# AWS S3
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
AWS_BUCKET_NAME=

# Email (Nodemailer)
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASS=
FROM_EMAIL=
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:5000/api
VITE_APP_NAME=PrepZero
```

---

## Notes

1. **Scalability**: The modular structure allows easy addition of new features
2. **Security**: JWT auth, rate limiting, input validation, and CORS configured
3. **Performance**: TanStack Query handles caching and background refetching
4. **Maintainability**: Separation of concerns with modules pattern
5. **Type Safety**: Consider adding TypeScript in future for better DX

---

*Last Updated: December 2024*

