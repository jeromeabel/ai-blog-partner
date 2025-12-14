# File Update Protocol

**When to update which files during the learning workflow**

---

## 📋 Quick Reference Table

| Event | Files to Update | What to Update |
|-------|----------------|----------------|
| **Session start** | None | Read PROGRESS.md, read current plan |
| **Start new task** | `PROGRESS.md` | Set "Active Task" and "Status" |
| | `plans/task_X_X_plan.md` | Create new plan file (Teacher provides template) |
| **Make architecture decision** | Current plan file | Document decision + rationale in "Architecture Decisions" section |
| **Complete subtask** | Current plan file | Check box in "Acceptance Criteria" |
| **Complete entire task** | `PROGRESS.md` | Check roadmap box ✅ |
| | `PROGRESS.md` | Add link to lesson file in "Lesson Index" |
| | `lessons/X_X-name.md` | Create new lesson file with learned concepts (Student writes, Teacher reviews) |
| | Current plan file | Move to `archive/` or delete |
| **Session end** | None | Clean exit |

---

## 🔄 Detailed Workflow

### Phase 1: Task Start

**Step 1: Teacher gives task**
```
Teacher: "Your next task is 2.2: Organization. Let me create the plan file for you."
Teacher creates: plans/task_2_2_plan.md
```

**Step 2: Student updates PROGRESS.md**
```markdown
**Active Task:** 2.2 Step 2 (Organizing)
**Status:** Planning → In Progress
**Plan File:** plans/task_2_2_plan.md
```

**Files updated:** `PROGRESS.md` (by Student)

---

### Phase 2: Planning & Architecture Decisions

**Step 1: Student reads plan file**
```bash
Read: plans/task_2_2_plan.md
Understand: Goal, questions, acceptance criteria
```

**Step 2: Student makes architecture decisions**
```
Student discusses options with Teacher
Student updates plan file with decisions
```

**Example update to plan file:**
```markdown
### Decision 1: LoopAgent vs Simple Agent?

**Decision:** Use simple Agent (not LoopAgent)

**Rationale:**
- Task is straightforward (reorganize chunks)
- Low quality variance (structural, not semantic)
- Faster execution without retry overhead
```

**Files updated:** `plans/task_2_2_plan.md` (by Student)

---

### Phase 3: Implementation

**Step 1: Student writes code**
```
Student implements based on plan
Student checks acceptance criteria as they complete subtasks
```

**Step 2: Student updates plan file**
```markdown
### Acceptance Criteria
- [x] Reads blog_outline from session state
- [x] Reads draft_ok from session state
- [ ] Produces reorganized draft
```

**Files updated:** `plans/task_2_2_plan.md` (by Student)

---

### Phase 4: Review

**Step 1: Student shows code to Teacher**
```
Student: "I've completed the implementation. Here's my code:"
[Shows code]
```

**Step 2: Teacher reviews**
```
Teacher: "Great work! The code follows the patterns correctly.
Let me ask some review questions to test understanding..."
[Review questions]
```

**Files updated:** None (review phase)

---

### Phase 5: Task Completion

**Step 1: Student updates PROGRESS.md**
```markdown
## Roadmap
- [x] 2.1 Step 1 (Draft to Outlines) → lessons/2.1-loopagent.md
- [x] 2.2 Step 2 (Organizing) → lessons/2.2-organization.md  ← Check box
- [ ] 2.3 Step 3 (Writing Loop)
```

**Step 2: Student creates lesson file**
```
Student creates: lessons/2.2-organization.md
Student writes learned concepts in their own words
Teacher reviews lesson file
```

**Step 3: Student archives plan file**
```bash
mv plans/task_2_2_plan.md archive/
# Or delete if not needed for reference
```

**Files updated:**
- `PROGRESS.md` (by Student - check box, add lesson link)
- `lessons/2.2-organization.md` (by Student, reviewed by Teacher)
- `plans/task_2_2_plan.md` (moved to archive by Student)

---

## 🎓 Teacher/Student Protocol

### Teacher Responsibilities
- ✅ Create initial plan file for new tasks
- ✅ Give guided tasks with context
- ✅ Review student's code
- ✅ Review student's lesson file (check for understanding)
- ✅ Ask review questions to test understanding
- ❌ Do NOT implement code yourself
- ❌ Do NOT update files yourself (except creating initial plan)

### Student Responsibilities
- ✅ Update PROGRESS.md (task status, checkboxes)
- ✅ Make architecture decisions (documented in plan file)
- ✅ Write implementation code
- ✅ Check acceptance criteria as you work
- ✅ Create lesson file when task completes
- ✅ Archive/delete completed plan files

---

## 📁 File Ownership

| File | Created By | Updated By | Reviewed By |
|------|-----------|-----------|-------------|
| `PROGRESS.md` | Teacher (initial) | Student | Teacher |
| `plans/*.md` | Teacher (template) | Student | Teacher |
| `lessons/*.md` | Student | Student | Teacher |
| Code files | Student | Student | Teacher |

---

## ⚠️ Common Mistakes

### Teacher Mistakes
- ❌ Creating lesson files (Student should write concepts)
- ❌ Implementing code (Student should implement)
- ❌ Checking boxes in PROGRESS.md (Student should update)

### Student Mistakes
- ❌ Not documenting architecture decisions
- ❌ Not updating plan file with progress
- ❌ Not creating lesson file after task completion

---

## 🔗 Related Files

- **GUIDE.md** - How to use the learning system (user manual)
- **PROGRESS.md** - Current status (dashboard)
- **plans/** - Current task details
- **lessons/** - Completed concepts (reference)
