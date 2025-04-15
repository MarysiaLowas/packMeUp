# PackMeUp

A web application that helps users pack efficiently for trips by generating personalized packing lists tailored to the type of trip, number of people, planned activities, and available luggage capacity.

## Table of Contents
- [Project Description](#project-description)
- [Tech Stack](#tech-stack)
- [Getting Started Locally](#getting-started-locally)
- [Available Scripts](#available-scripts)
- [Project Scope](#project-scope)
- [Project Status](#project-status)
- [License](#license)

## Project Description

PackMeUp is designed to solve common problems users face when packing for trips:
- Difficulty remembering all necessary items
- Optimizing limited luggage space
- Adapting luggage contents to trip specifics (climate, activities, accommodation)
- Packing for multiple people simultaneously (e.g., families with children)

The application solves these problems through:
- A comprehensive survey collecting all relevant trip information
- AI-generated personalized packing lists
- Creation and storage of custom special lists
- Managing the packing process by marking items as packed

### Target Audience
- Families with children planning trips together
- Backpackers needing to optimize backpack contents

### Key Features
- Survey system to collect trip information
- Manual creation of special lists
- AI-generated packing lists
- Management of generated lists
- User account system

## Tech Stack

### Frontend
- Astro 5 - Fast, efficient pages and applications with minimal JavaScript
- React 19 - For interactive components
- TypeScript 5 - Static typing and better IDE support
- Tailwind 4 - Utility-first CSS framework
- Shadcn/ui - Accessible React component library

### Backend
- FastAPI - High-performance Python web framework
- SQLAlchemy - SQL toolkit and ORM
- PostgreSQL - Relational database

### AI Integration
- Openrouter.ai - Access to various AI models (OpenAI, Anthropic, Google)

### CI/CD & Hosting
- Github Actions - CI/CD pipelines
- Render - Application hosting

## Getting Started Locally

### Prerequisites
- Node.js v22.14.0 (use a Node version manager like nvm or volta)
- npm or yarn

### Installation

1. Clone the repository
```bash
git clone git@github.com:MarysiaLowas/packMeUp.git
cd pack-me-up
```

2. Install the correct Node.js version
```bash
# If using nvm
nvm use
```

3. Install dependencies
```bash
npm install
```

4. Start the development server
```bash
npm run dev
```

5. Open your browser and navigate to `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start the development server
- `npm run build` - Build the application for production
- `npm run preview` - Preview the production build locally
- `npm run astro` - Run Astro CLI commands
- `npm run lint` - Run ESLint to check code quality
- `npm run lint:fix` - Run ESLint and fix issues automatically
- `npm run format` - Format code with Prettier

## Project Scope

### Included in MVP

- Survey system for collecting trip information
- Manual creation of special packing lists
- AI-generated packing lists based on trip parameters
- List management (adding, removing, marking items)
- User account system with registration and login
- Profile management
- Password recovery
- History of created lists

### Not Included in MVP

1. Advanced luggage packing algorithm
2. Multimedia support (photos of items, instructional videos)
3. List sharing between users
4. Mobile applications (web version only)
5. Interfaces in languages other than English
6. Social features (comments, list ratings)

## Project Status

Current version: 0.0.1 (Initial development)

The application is being developed with the following success criteria in mind:

### Product Metrics
- 75% of AI-generated lists accepted without major modifications
- Users modify no more than 75% of generated list content
- Average of at least 2 special lists created per active user

### Technical Criteria
- 99.5% system availability
- Proper functioning across all popular browsers (Chrome, Firefox, Safari, Edge)
- Responsive interface for different screen sizes (desktop, tablet)
- Average page load time under 5 seconds

### Development Timeline
- Application to be created within 5 weeks of part-time work for one person

## License

This project is licensed under the [MIT License](LICENSE). 