# Changelog

All notable changes to this project will be documented in this file.

**[中文更新日志](./CHANGELOG.zh-CN.md)**

---

## [2.1.2] - 2025-06-26

### Fixed
- Fixed the display of error messages.
- Fixed the back-end judging logic for text problems.

---

## [2.1.1] - 2025-06-25

### Fixed
- Fixed a bug that prevented problems from being deleted.
- Resolved an issue where API requests for problems with identical names could return one same data.

---

## [2.1.0] - 2025-06-24

### Changed

- Merged the frontend and backend repositories into a single Monorepo.

---

## [2.0.1] - 2025-06-24

### Added
- Added a regular check to validate the result of regex search for AI's output.

### Fixed
- Fixed an issue where the allow_ai option was incorrectly displayed for choice problems.
- Resolved a bug in the backend auto-judging logic for choice problems and text problems.

---

## [2.0.0] - 2025-06-20

### Added
- **Complete API Token Management System**: Integrated into a new "System Settings" page, this feature allows users (teachers and above) to perform CRUD operations on their AI platform tokens. Critical actions are secured with password verification, and tokens are desensitized on the frontend for security.
- **On-Demand AI Evaluation**: Teachers can now enable or disable AI-assisted grading on a per-question basis. This includes assigning a specific token to each question, enabling the flexibility to use different AI models for different problems.
- **Smart & Flexible Prompt Generation**: A new system allows teachers to set configurable scoring parameters and guidelines for each question. The system then automatically combines these settings with pre-built templates and question content to generate tailored prompts for the AI.
- **Context-Aware AI Interaction**: Implemented an `AI-History` model to persist the interaction history for each question separately. This context is automatically loaded in subsequent requests to ensure grading consistency and stability over multiple turns.
- **Multi-Platform AI Proxy Service**: A new `ai_sandbox` Docker container acts as a universal proxy. It can dynamically select the appropriate platform SDK based on request parameters, making the system highly extensible for integrating new AI services in the future.

---

## [2.0.0-alpha] - 2025-04-09

### Added
- Implemented a basic Docker sandbox for AI-powered code evaluation. (Note: Not yet integrated with the project backend).
- Utilizes the `gpt-4o` model via the OpenAI platform to perform code scoring.
- Created a pre-built prompt for AI-driven code review.
- Introduced 5 configurable parameters for scoring related to code implementation and code style.


---

## [1.0.0] - 2024-03-22

### Added
- Implemented basic CRUD (Create, Read, Update, Delete) functionalities for course-based assignments.
- Added support for multiple question types:
    - **Multiple-choice:** Supports both single and multiple correct answers.
    - **Short-answer:** Supports manual grading only in this version.
    - **Programming:**
        - Supports `cpp` and `java` languages with multi-file submissions (within the same directory).
        - Allows configuration of command-line arguments, standard input, time limits, and memory limits.

