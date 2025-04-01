# Company Research Agent PRD

## 1. Overview

### **Product description and purpose**

Web app that speeds up company research. Provides the user with an overview of the company that they can digest in less than five minutes and can create a page in the user’s database of choice with the information provided. 

### **Target users**

Anyone who wants to know more about a company. Users may be searching for a job or just interesting in learning more about a company.

### **Key success metrics**

- **Time to Research:** Reduce user research time from 20 minutes to less than 1 minute
- **Time to Record:** Reduce user input time from 5 minutes to less than 1 minute

## 2. Requirements

### Core features (prioritized)

- **Company Overview:** Automatically provides a user with a basic overview of a company and resources to dig deeper. Basic Overview Includes:
    - Link to Company Website
    - Link to Company LinkedIn
    - Company Summary
    - Company Purpose
    - Key Products & Features
    - Competitors
    - Private, Public
        - If Private & Venture Funded, Funding Rounds & $ raised
    - News - Links to the most recent or most relevant articles about the company
    - Videos - Links to product overviews or demos on Youtube
- **Integration:** Uploads content from company overview to a platform of the users choice. Options are Notion and Google (Docs)
    - This feature is dependent upon the user linking their account to the application. If they decide not to link it, the company overview can be provided as a pdf.
- Additional Features
    - Provides the user with recommended follow-up questions.
    - Looks at the company research database to see if there are any companies you’ve previously researched that are connected to this company in some way.
    - Asks the user if they would like an overview of any of the competing companies
    - Provides the user with recommended questions to ask during an interview with this company.
    - Provide the user with an option to export this page to Notion
    - After pushing initial content to a page, user can choose to push more content to the page based on follow up questions.
    - Set up notification for a company. Sends user an email weekly with any new articles about the company are released.

### Technical Constraints

- **Response Time:** Build and reply with a company overview in less than one minute.
- **Integration:** Integrate with Notion and Notion databases.
- **Hosting:** Needs to be able to be hosted on the cloud.
- **Optional:**
    - Compatibility: Compatible on mobile or desktop

### Key user flows:

[https://www.figma.com/board/sjcnqVnSzuxScqMJ1skpsl/AI-Tool-Workflow-Designs?node-id=14-204&t=4YfmeRph1acAmAN9-0](https://www.figma.com/board/sjcnqVnSzuxScqMJ1skpsl/AI-Tool-Workflow-Designs?node-id=14-204&t=4YfmeRph1acAmAN9-0)

## 3. Design & UX

### Critical UI components

- Search/Prompt Bar: Basic input bar for user
- Nice to Have:
    - ‘Push to [Application]’ Button - A button or keyboard shortcut to push the content to the selected application.
        - Alternative: Typing and entering ‘Yes’ when prompted by application to push the content to [application]

### Basic wireframes

- Keep it simple, think AI Tool UI interface (Claude, ChatGPT)

## 4. Implementation

### Timeline

- Deploy v1: April 1, 2025
- Deploy v2: April 2, 2025

### Dependencies

- N/A

### Team resources

- Perry’s Time

[Process Overview](https://www.notion.so/Process-Overview-1c7db18c766280f6bfaac72e25a33ebd?pvs=21)