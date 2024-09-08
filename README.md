<p align="center">
  <img src="static/images/favicon/apple-touch-icon.png" alt="Voyage Vista Logo">
</p>
<h1 align="center">Voyage Vista</h1>

<h2>Welcome</h2>

Link to live website: [CLICK HERE!](https://ckz8780-django-voyagevista-app-19845c20e94f.herokuapp.com/)

![Am I Responsive Image](documentation/screenshots/responsive.JPG)

# Introduction
Voyage Vista is a dynamic blogging platform tailored for travelers, adventurers, and enthusiasts of exploration. Designed with both content creators and readers in mind, Voyage Vista offers a user-friendly experience for sharing and discovering stories, tips, and insights about travel. Built using the Django web framework, the platform facilitates a seamless interaction between users, allowing them to create, share, and engage with content on various travel-related topics.

Voyage Vista is not just another blog; it’s a community-driven platform that connects people who share a passion for travel and exploration. Whether you're looking to share your latest adventure, find accommodation tips, or gather travel advice, Voyage Vista provides the perfect space for you.

## Categories on Voyage Vista
To ensure that content is well-organized and easily navigable, Voyage Vista offers specific categories under which users can classify their posts. These categories help users find content that matches their interests:
- **Destinations:** This category features posts about various travel destinations around the world. Whether you’re looking for a guide to a popular city or exploring hidden gems, this category is a treasure trove of travel inspiration.
- **Accommodation:** Finding the right place to stay is a crucial part of any travel experience. Posts in this category offer advice, reviews, and tips on various types of accommodation, from luxury hotels to budget-friendly hostels.
- **Travel Tips:** This category is packed with practical advice to make your travels smoother and more enjoyable. From packing tips to navigating foreign cultures, these posts are essential reading for both novice and seasoned travelers.
## Features of Voyage Vista
Voyage Vista is designed to provide a rich and engaging experience for both writers and readers. The platform includes a variety of features that enhance the overall user experience:

- **User Registration and Authentication:**

Users can easily sign up, create an account, and manage their profiles. Secure login and logout functionalities ensure that user data remains private and safe.

![Registration Image](static/documentation/signup.png)

- **Post Creation and Management:**

Registered users can create and publish blog posts with ease. The platform provides an intuitive editor, allowing users to craft well-structured posts with images and text.
Users can edit their posts even after publication, ensuring that the content remains up-to-date and accurate.
- **Comments and User Interactions:**

Readers can engage with posts by leaving comments, which fosters a community discussion around the content. Comment moderation tools allow authors and admins to maintain a positive environment.
Users can like posts and save their favorite content for easy access later.
- **Categories:**

All posts are organized into predefined categories—Destinations, Accommodation, and Travel Tips—making it easy for users to browse and discover content based on their interests.
Search Functionality:

A robust search feature allows users to find posts by entering keywords. This helps in quickly locating specific content without having to browse through the entire site.
- **User Dashboard:**

Each user has a personalized dashboard where they can manage their posts, likes, and saved articles. This centralized view makes it easy for users to track their contributions and interactions on the platform.

![Dashboard Image](static/documentation/dashboard.png)

- **Responsive Design:**

The platform is fully responsive, ensuring a seamless experience across all devices, whether accessed via desktop, tablet, or smartphone.
Admin Panel:

The admin panel allows site administrators to manage users, posts, comments, and categories efficiently. Admins can approve or reject posts and comments, ensuring the quality of content on the site.
- **Media Management:**

Integrated with Cloudinary, Voyage Vista allows users to easily upload, manage, and display images in their posts, enriching the visual appeal of the content.
- **SEO-Friendly:**

The platform is optimized for search engines, helping posts gain visibility and attract more readers organically.
- **Error Handling and Notifications:**

Comprehensive error handling ensures that users are guided through any issues they encounter with clear notifications and prompts.

![Error handling Image](static/documentation/error.png)

# Contents
- [Introduction](#introduction)
    - [Categories on Voyage Vista](#categories_on_voyage_vista)
    - [Features of Voyage Vista](#features_of_voyage_vista)
- [UX - User Experience](#ux---user-experience)
    - [User Goals](#user_goals)
    - [UX Design Principles](#ux_design_principles)
- [Design](#design)
  - [Colour Scheme](#colour-scheme)
  - [Fonts](#fonts)
    - [Google Fonts](#google-fonts)
    - [Usage](#usage)
- [Project Planning](#project-planning)
  - [Strategy Plane](#strategy-plane)
  - [Agile Methodologies - Project Management:](#agile-methodologies---project-management)
    - [MoSCoW Prioritization:](#moscow-prioritization)
    - [User Stories, Milestones and Epics](#user-stories-milestones-and-epics)
      - [Users Stories](#users-stories)
      - [Milestones](#milestones)
      - [Epics](#epics)
  - [Scope Plane](#scope-plane)
  - [Structural Plane](#structural-plane)
  - [Framework & Aesthetic Layout](#framework--aesthetic-layout)
    - [Wireframes](#wireframes)
      - [Home Page Wireframes](#home-page-wireframes)
      - [Post Detail Page Wireframes](#post-detail-page-wireframes)
      - [Sign up form wireframe](#signup-form-wirefram)
      - [Log in wireframe](#log-in-wireframe)
      - [Add post wirefram](#add-post-wireframe)
      - [My Posts wireframe](#my-posts-wireframe)
      - [My Likes wireframe](#my-likes-wireframe)
      - [My Comments wireframe](#my-comments-wireframe)
      - [My Bookmarks wireframe](#my-bookmarks-wireframe)
      - [Sign out wireframe](#sign-out-wireframe)
      - [About us & Contact us wirefram](#about-us-contact-us-wireframe)
    - [Database Schema - Entity Relationship Diagram](#database-schema---entity-relationship-diagram)
      - [Database Schema](#database-schema)
      - [Entity Relationship Diagram (ERD)](#entity-relationship-diagram-erd)
      - [Tables Overview](#tables-overview)
      - [Relationships](#relationships)
      - [Design Considerations](#design-considerations)
- [Project Features](#project-features)
  - [Existing Features](#existing-features)
  - [User Interface and Page Overview](#user-interface-and-page-overview)
    - [Homepage](#homepage)
    - [User Registration](#user-registration)
    - [Login and Logout](#login-and-logout)
    - [User Dashboard](#user-dashboard)
    - [Add Post](#add-post)
    - [Post Details](#post-details)
    - [Search Functionality](#search-functionality)
    - [Comment and Interactions](#comment-and-interactions)
    - [Categories](#categories)
    - [My Bookmarks](#my-bookmarks)
    - [My Likes](#my-likes)
    - [My Comments](#my-comments)
    - [My Posts](#my-posts)
    - [Pagination](#pagination)
    - [Footer](#footer)
    - [Admin Panel](#admin-panel)
    - [Contact & About us](#contact--about-us)
  - [Future Considrations](#future-considerations)
- [Technology Used](#technology-used)
  - [Frontend](#frontend)
  - [Backend](#backend)
  - [Deployment and Version Control](#deployment-and-version-control)
  - [Development Tools](#development-tools)
  - [Libraries and Frameworks](#libraries-and-frameworks)
  - [Validation Tools](#validation-tools)
  - [Others](#others)
- [Testing](#testing)
- [Deployment](#deployment)
  - [GitHub](#github)
  - [Gitpod](#gitpod)
  - [Heroku](#heroku)
  - [Database](#database)
  - [Cloudinary Integration](#cloudinary-integration)
- [Cloning and Forking](#cloning-and-forking)
  - [Cloning the Repository](#cloning-the-repository)
  - [Forking the Repository](#forking-the-repository)
- [Credits](#credits)
  - [Code](#code)
  - [Media](#media)
  - [Acknowledgements](#acknowledgements)

  ## UX- User Experience
The user experience (UX) on Voyage Vista is thoughtfully designed to cater to both seasoned travelers and those new to the world of blogging. Every aspect of the platform is crafted with the user in mind, ensuring an intuitive, engaging, and seamless experience. Here’s an in-depth look at the UX design considerations for Voyage Vista:

### User Goals
Voyage Vista is designed to help users achieve their goals quickly and efficiently:

- **Discovering Travel Content:** Users can easily find posts that match their interests through categories, search functionality, and related posts.
- **Sharing Experiences:** Content creators can effortlessly publish posts, upload images, and manage their content.
- **Engaging with the Community:** Users can comment on posts, like content, and save articles for future reference, fostering a sense of community.
- **Finding Relevant Information:** The platform offers a structured layout that allows users to quickly locate the information they need, whether it's a travel tip, accommodation advice, or destination guide.

### UX Design Principles
Voyage Vista’s UX is built around key design principles to ensure a positive experience for all users:

- **Simplicity:** The platform features a clean, uncluttered design that makes navigation straightforward. Users can easily find what they’re looking for without unnecessary distractions.
- **Consistency:** A consistent layout, color scheme, and typography are used throughout the site to create a cohesive and familiar experience for users as they browse different pages.
- **Responsiveness:** The website is fully responsive, ensuring that users have a smooth experience whether they’re accessing it from a desktop, tablet, or mobile device.
- **Accessibility:** Voyage Vista is designed to be accessible to all users, including those with disabilities. Features like alt text for images, clear headings, and an intuitive navigation structure make the platform easy to use for everyone.

# Design
Voyage Vista’s design is crafted to enhance user engagement and provide a visually appealing and functional experience. The design elements focus on creating a cohesive and immersive environment that complements the website's travel content.

## Color Scheme
The colour scheme of Voyage Vista is inspired by a refreshing travel aesthetic, incorporating a palette that reflects tranquility and adventure. Key colors include:

- **Primary Color:** A calming teal (#23bbbb) used for navigation bars and buttons, creating a soothing visual experience.
- **Accent Colors:** Complementary shades like dark teal (#1fa3a3) and white for text and backgrounds, ensuring readability and contrast.
- **Neutral Colors:** Subtle greys and off-whites for backgrounds and secondary elements, maintaining a clean and professional look.
The chosen colors enhance the website's overall ambiance, aligning with the theme of exploration and travel.

![Color Scheme Image](static/documentation/color_scheme.png)

## Fonts
Voyage Vista employs a well-selected combination of fonts to ensure readability and aesthetic appeal.

- **Google Fonts**
    - Roboto: A versatile and modern font used for body text. It features a balanced design that improves readability and accessibility.
    - Lato: This font complements Roboto and is used for headings and subheadings. Its slightly rounded design provides a friendly and approachable feel.
- **Usage:**
    - Roboto: Applied for general content, including articles and descriptions, ensuring clear and easy-to-read text.
    - Lato: Used for headings, navigation items, and call-to-action buttons, adding emphasis and improving visual hierarchy.
By integrating these fonts, Voyage Vista achieves a harmonious design that enhances the user experience through clear, readable text and a visually appealing layout.

# Project planning

## Strategy Plane
The strategy plane involves defining the high-level goals and objectives of the project. It includes understanding user needs, business requirements, and project constraints to create a roadmap that guides development. For VoyageVista, this means ensuring that our blog platform meets user expectations for usability, functionality, and design while aligning with business goals.

### Agile Methodologies - Project Management

  Story Points Allocation Story points are used to estimate the effort required to complete user stories or tasks. Each story point represents a unit of work or complexity, helping the team understand the relative effort needed. In VoyageVista, this means assigning points to tasks like developing new features, fixing bugs, or making design changes.
  - Sprint Planning Example:

    Here is an example of how story points are managed and allocated across different categories in sprints:
    - Total Story Points for the Sprint: 128
    - Must-have Points: 81 (63.3% of the total)
    - Should-have Points: 28 (21.9% of the total)
    - Could-have Points: 19 (14.8% of the total)

    - Example Milestones:
    - Milestone 1: User Engagement
  - Total Story Points: 46
  - Breakdown:
    - Must-have: 21 points
    - Should-have: 8 points
    - Could-have: 17 points
    - Milestone 2: Content Discovery
  - Total Story Points: 35
  - Breakdown:
    - Must-have: 22 points
    - Should-have: 13 points

### MoSCoW Prioritization

MoSCoW is a prioritization technique used to classify requirements into categories:

- **Must Have:** Essential features that are critical for the project's success.
- **Should Have:** Important but not crucial; they add significant value.
- **Could Have:** Desirable features that are not critical and can be included if time permits.
- **Won't Have:** Features that are not necessary for the current project phase.
For VoyageVista, "Must Have" might include user authentication and post creation, while "Could Have" could include advanced search filters, dashboard and sorting options.

## User Stories, Milestones and Epics
### User stories
User Stories are concise descriptions of tasks or needs from the user's perspective. They are written in plain language, focusing on what the user wants to achieve and the value or outcome they seek, rather than technical details.

| Title | User Story | MoSCoW Priority | Milestone |
|-------|------------|----------|-----------|
| Seamless sign up Experience | As a user, I **want** a seamless **sign-up** experience so that I can quickly **create** an account and start using the website without any hassle. | **MUST HAVE** | User Authentication |
| Logout | As a **registered user**, I want to **log out** securely, so that my **account remains safe** when I am not using it. | **MUST HAVE** | User Authentication |
| Add Post | As a **registered user**, I want to be able to **add a new post** easily, so that I can **share** my thoughts or content with others. | **MUST HAVE** | User Engagement |
| Create drafts | As a **website owner**, I want the ability to **create** draft posts, so that I can **work on writing** the content gradually and finalize it at a later time. | **MUST HAVE** | Content Mangement and Moderation |
| Seamless Login Experience | As a **registered user**, after logging in, I **expect** the login and sign up buttons to **disappear** from the navigation bar, and a sign out button to **appear** instead. | **MUST HAVE** | User Authentication |
| My Likes | As a **registered user**, I want to **see** a list of all the posts I have liked, so that I can easily **access** content that I found interesting or valuable. | **SHOULD HAVE** | User Engagement |
| Browse Posts with Pagination | As a user, I want to **view a paginated list** of posts, so that I can easily **navigate through** multiple posts and select which ones I want to read. | **SHOULD HAVE** | Content Discovery |
| Browse Categories | As a **user**, I want to easily **find blog posts** on topics of interest by browsing through different categories so that I can quickly **access** content that is relevant to me. | **SHOULD HAVE** | Cotent Discovery |
| Easy Contact Option | As a **registered user**, I want to easily **contact** the website administrators so that I can **make inquiries** or provide feedback. | **SHOULD HAVE** | Cotent Discovery |
| Quick Search Functionality | As a **user**, I want to **search** for specific destinations, hotels, or adventures, so I can **find** relevant information quickly. | **SHOULD HAVE** | Cotent Discovery |
| Rating Posts | As a **registered user**, I want to **rate** destinations, hotels, and adventures based on my experiences so that I can **share** my feedback and help others make informed decisions. | **COULD HAVE** | User Engagement |
| Delete Comments | As a **registered user**, I want to be able to **delete** my comments on a post so that I **have control** over my participation in discussions and can remove comments I no longer wish to be associated with. | **COULD HAVE** | User Engagement |
| Bookmarking | As a **registered user**, I want to **bookmark** posts or destinations that I **find** interesting so that I can easily reference them in the future. | **COULD HAVE** | User Engagement |
| My Bookmarks | As a **registered user**, I want to **access** a list of posts I have bookmarked, so that I can quickly **find** content I saved for later. | **COULD HAVE** | User Engagement |
| Edit comments on a post | As a **registered user**, I want to be able to **edit** my comments on a post so that I can **correct** or clarify my contributions, ensuring they remain accurate and relevant. | **COULD HAVE** | User Engagement |


### Milestones
Milestones in a project serves as a key checkpoint or goal along the project's timeline. It signifies the completion of a major phase, the achievement of a crucial objective, or the meeting of an important deadline. Milestones are essential for monitoring progress, setting deadlines, and ensuring alignment among team members and stakeholders regarding major project events or accomplishments. Unlike individual tasks or user stories, milestones do not involve direct work but act as indicators that a significant portion of the project has been completed.

### Epics
Epics are large bodies of work that can be broken down into smaller, more manageable tasks or user stories. They represent significant features or functionalities that contribute to the overall goal of the project.

- User Engagement and Interaction

  - Description: This epic encompasses all user interactions with posts, comments, and personal engagement features.
  - Associated User Stories:
    - Rating posts.
    - Delete comments on a post.
    - Edit comment on a post.
    - Bookmarking.
    - Edit post.
    - Delete post.
    - Like/Unlike posts.
    - My Cooments.
    - My Likes.
    - My Bookmarks.
    - My Posts.
    - Leave a comment.
    
- Content Discovery and Management

  - Description: This epic includes all functionalities related to discovering, browsing, and managing content on the platform.
  - Associated User Stories:
      - Browsing categories.
      - Open Post.
      - Browsing posts without login.
      - Browse posts with pagination.
      - Easy Contact Option.
      - Quick Search Functionality.
      - Browse and Discover New Travel Experiences.

- User Authentication and Account Management

  - Description: This epic covers all features related to user authentication, registration, and account management.
  - Associated User Stories:
    - Seamless Signup Experience.
    - Logout.
    - Seamless Login Experience.
    - Implement Authentication State Handling.

- Content Management and Moderation
  - Description: This epic focuses on all functionalities related to managing, moderating, and curating content on the platform.
  - Associated User Stories:
    - Moderate User-Generated Content.
    - Manage Recommended Content.
    - Approve Comments.
    - Create drafts.

# Scope Plane

In project management and design, the Scope Plane defines the boundaries and deliverables of a project. It is essential for ensuring that all project stakeholders have a clear understanding of what is included and excluded from the project's scope. Here's an overview of the Scope Plane in the context of your project:

- Project Boundaries
In-Scope: Defines what functionalities, features, and elements are included in the project. For instance, in your project, this includes user authentication, content management, rating systems, and user engagement features.
Out-of-Scope: Clarifies what is not included in the project. For example, advanced content filtering and interactive maps integration are noted as future considerations or not part of the current project scope.
- Deliverables
Functional Requirements: Detailed specifications of what the system should do. These include user stories like rating posts, browsing categories, and viewing ratings.
Non-Functional Requirements: Aspects like performance, security, and usability that the project must meet. This includes responsiveness, data protection, and a seamless user experience.
- Project Objectives
Primary Objectives: Achieve core functionalities such as user registration, content creation, and interaction with posts (e.g., commenting, liking).
Secondary Objectives: Enhancements and additional features that improve the user experience, like custom branding and backup solutions.

- Stakeholder Expectations
User Stories: Capture the needs and expectations of users, ensuring that the project deliverables meet these requirements.
Acceptance Criteria: Define how the success of the deliverables will be measured, ensuring that each feature meets the defined user needs.
- Scope Management
Scope Control: Procedures to manage changes and ensure that the project remains within the defined scope. This includes handling requests for additional features or modifications.
Scope Verification: Regular reviews and validation to confirm that project deliverables align with the agreed-upon scope.

- Exempel from Voyage Vista Project:
    - In-Scope:

      - User registration and authentication
      - Rating and commenting on posts
      - Bookmarking and saving posts
      - Browsing and discovering posts by categories
    - Out-of-Scope:

      - Advanced content filtering
      - Interactive maps integration

The Scope Plane ensures that all project aspects are well-defined and understood, helping to avoid scope creep and ensuring that the project delivers what is expected within the agreed-upon constraints.


