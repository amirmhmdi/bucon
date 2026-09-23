# BUCON

[View Live Site](https://bucon-codeinstitute-2af3aed47d58.herokuapp.com/)

BUCON is a Django-based construction company website designed to present a business online, share project work, publish updates, and manage internal operations for staff and managers. The platform brings together a public-facing portfolio and blog, a contact workflow for enquiries, and a private operations area for labor tracking, approvals, and payroll reporting.

![BUCON project overview](documents/github_project.png)

_Project planning snapshot for the BUCON application and its core management workflow._

![Responsive mockup of the BUCON site](documents/amiresponsive.png)

_Responsive multi-device mockup showing the BUCON site across desktop, tablet, and mobile layouts._

## Contents

- [Overview](#overview)
- [UX](#ux)
  - [User Stories](#user-stories)
  - [Strategy](#strategy)
  - [Scope](#scope)
  - [Structure](#structure)
  - [Skeleton (Wireframes)](#skeleton-wireframes)
  - [Surface](#surface)
- [Design](#design)
  - [Typography](#typography)
  - [Colour Scheme](#colour-scheme)
  - [Imagery](#imagery)
- [Website Features](#website-features)
- [Tablet/Mobile View](#tabletmobile-view)
- [Future Features](#future-features)
- [Technologies Used](#technologies-used)
- [Deployment](#deployment)
- [Testing](#testing)
- [Credits](#credits)

## Overview

BUCON is built for a small construction business that needs a clear and professional online presence. Visitors can learn about the company, browse completed work, read project updates, and send enquiries through a contact form. Staff and managers use separate parts of the application to manage hours, approvals, payroll, and site content without needing to change code.

The project uses Django as the core framework and includes a role-based structure for public visitors, labor users, managers, and admin users. It is designed to be practical, secure, and easy to maintain while still feeling polished and professional for a construction brand.

## UX

### User Stories

The following user stories describe the main needs of the application and are grouped by feature area. They explain how the site supports visitors, staff, managers, and administrators in everyday use.

#### Epic 1: Project Foundation

##### 1. Project foundation and role model

This story creates the base for the application. BUCON is built as a Django project with separate apps for accounts, content, portfolio work, timesheets, and dashboard management. A shared profile model is linked to each user so that the project can distinguish between labor staff, managers, and administrators.

Key requirements:

- The project uses Python 3.12 and Django 4.2.30.
- Core apps include `accounts`, `core`, `blog`, `portfolio`, `timesheets`, and `dashboard`.
- Authentication, forms, rich-text editing, media management, static hosting, and deployment tools are installed and configured.
- Each user has a profile with role, contact, employment, and security fields.
- A profile is created automatically whenever a new user is added.

##### 2. Shared layout and navigation

This story ensures the site looks consistent and feels familiar across every page. Visitors see a public layout, while logged-in staff and managers see navigation options that match their responsibilities.

Key requirements:

- The main navigation always includes Home, Portfolio, About Us, and Contact Us.
- Logged-out visitors see a login link.
- Labor users see access to timesheet features.
- Manager users see access to dashboard tools.
- Footer content is pulled from the site settings model.

#### Epic 2: Site Content Foundations

##### 3. Site settings and company details

This story gives administrators a simple way to maintain the business information without editing templates or code. The site footer and about section are therefore controlled through a single data source.

Key requirements:

- Site settings are managed as a single editable record.
- About content uses a rich-text editor for easier formatting.
- Brand logo and contact information are managed centrally.

##### 4. Homepage banner management

This story allows the business to control what is shown on the homepage. Banner content can be created, edited, and ordered by the admin without requiring a developer to change code.

Key requirements:

- Admin users can create and update homepage banners.
- Only active banners appear on the front page.
- Banners are displayed in a defined order.

#### Epic 3: Public Website

##### 5. Home page experience

This story focuses on the first impression of the site. The homepage presents the company clearly, gives visitors a reason to trust the brand, and gives them a simple path to enquire or explore work.

Key requirements:

- A hero carousel appears at the top of the page.
- Featured portfolio items are shown on the homepage.
- Company information and call-to-action content are displayed.
- A contact form is visible for enquiries.
- The page remains responsive for different screen sizes.

##### 6. Portfolio browsing

This story helps visitors explore completed projects and understand the standard of work delivered by the company. A portfolio list gives a clear overview, and each project has a dedicated detail page with more information.

Key requirements:

- Only published projects appear in the public list.
- Each project has a unique page slug.
- Project pages show description, images, completion details, and client information where needed.

##### 7. Blog reading experience

This story introduces an editorial section where the business can share updates, milestones, and project insights. Visitors can browse and read published posts in a clean, readable layout.

Key requirements:

- Only published blog entries are shown publicly.
- Posts are displayed in reverse chronological order.
- Individual post pages show the article, author, and publication date.
- The blog list is paginated for easy reading.

##### 8. Contact form for enquiries

This story allows potential clients to get in touch without exposing staff contact details in public templates. The message is stored securely and can be reviewed by management later.

Key requirements:

- Visitors submit their name, email, and message.
- Contact submissions are saved as enquiry records.
- The form provides a clear success message after submission.

#### Epic 4: Authentication and Accounts

##### 9. Manager-led labor account creation

This story gives managers a controlled way to create staff accounts for labor roles. Each new account is created with a temporary starting password and the correct user role.

Key requirements:

- Managers create labor accounts with email and temporary password.
- New users are assigned the labor role.
- Temporary-password enforcement is enabled for first-time login.
- Accounts are created as active employees by default.

##### 10. Password reset for labor users

This story ensures managers can support staff who need account access restored or reset. A temporary new password is set when necessary, and the user is forced to change it on next login.

Key requirements:

- Managers can reset a labor password.
- Password resets require a new temporary password.
- The forced change flag is re-enabled after reset.
- Managers cannot reset admin or manager passwords through labor controls.

##### 11. Forced password change on first login

This story protects the system by requiring staff to change temporary passwords before continuing. It prevents onboarding users from using a system-generated password beyond the initial login screen.

Key requirements:

- Users with a temporary password are redirected to a password-change page.
- Access to protected areas is blocked until the password is updated.
- The password-change flag is cleared after use.

##### 12. Email-based login

This story keeps account access simple and secure. Users authenticate with their email address instead of a username, and the app redirects them according to role once they are signed in.

Key requirements:

- Login uses email-based authentication.
- Invalid credentials show clear feedback.
- Successful login routes staff to the correct area.
- Public self-registration is disabled.

#### Epic 5: Labor Timesheet Area

##### 13. Daily timesheet submission

This story allows labor staff to record their daily work details. The system calculates hours automatically and keeps a clear record for approval and payroll.

Key requirements:

- Users enter date, start time, end time, break duration, and work description.
- Total hours are calculated automatically.
- New entries are marked as pending.
- Staff can only create entries for themselves.
- Duplicate shifts are prevented.

##### 14. Editing pending or rejected timesheets

This story gives labor staff the ability to correct mistakes while entries are still being reviewed. Once an entry is approved, a tighter restriction is enforced.

Key requirements:

- Pending or rejected entries can still be edited.
- Approved entries are locked.
- Rejected entries can be corrected and sent back to pending status.

##### 15. Timesheet history

This story helps workers track their own work history and understand the status of each submission. The history view makes it easy to review current and past entries.

Key requirements:

- Users can see a list of their own timesheet entries.
- Dates, hours, description, and status are displayed clearly.
- Manager rejection reasons are visible when present.
- Approved entries are displayed in a read-only format.

#### Epic 6: Manager Dashboard

##### 16. Review and approve timesheets

This story gives managers control over labor submissions. A review screen makes it easy to approve or reject work based on the information provided by staff.

Key requirements:

- Managers see pending entries across all labor staff.
- Entries can be approved or rejected.
- Approval stores the approving user and timestamp.
- Rejection requires a reason.
- Dashboard views are restricted to manager-level users.

##### 17. Contact message review

This story allows managers to review enquiries submitted through the public contact form and respond as needed. It keeps the inbox organised and helps identify unread messages quickly.

Key requirements:

- Message records are displayed in reverse chronological order.
- Managers can mark messages as read.
- Unread items are clearly distinguished in the interface.

##### 18. Labor account management

This story keeps labor information up to date without allowing managers to change a staff member's role. It gives the management team control over day-to-day employment details.

Key requirements:

- Managers can update hourly rate, phone number, and employment status.
- Inactive staff cannot log in or submit new entries.
- A labor user's role remains protected.

##### 19. Payroll reporting

This story turns approved timesheet data into a useful payroll summary. Managers can view totals for a chosen date range and export the results for further processing.

Key requirements:

- Approved hours are aggregated over a date range.
- Estimated pay is calculated using the labor rate.
- Reports are visible in the dashboard.
- CSV export is available for payroll workflows.

#### Epic 7: Admin Content Management

##### 20. Manager promotion workflow

This story allows administrators to promote a trusted user to a managerial role. Once promoted, the user can access management features after their next login.

Key requirements:

- Admins can update a user's role to manager.
- Promotion grants access to the management area.
- Role changes are reflected immediately after login.

##### 21. Blog content management

This story gives the business a simple way to publish or update editorial content. Admin users can maintain the blog without needing to touch the codebase.

Key requirements:

- Posts can be created, edited, published, and removed.
- Rich-text editing is available for article content.
- Posts can be saved as draft or published content.

##### 22. Portfolio content management

This story supports the promotion of project work on the public site. Portfolio items can be defined with rich content and multiple gallery images, making it easy to showcase completed jobs.

Key requirements:

- Projects can be created, updated, published, and deleted.
- Each project includes a description and visual media.
- Multiple project images can be uploaded per item.
- Projects can be marked as featured and published.

![Project planning and dashboard imagery](documents/features/dashboard_page_feature.png)

_The dashboard and project-planning visuals reflect the operational workflow used by managers and administrators._

### Strategy

#### Visitor goals

- Understand the company and review completed work.
- Find contact details and send a message.
- Browse recent portfolio items and read blog posts.

#### Labor goals

- Sign in securely and submit timesheets on time.
- Review prior entries and confirm approval status.
- Complete a required password change and access the staff area safely.

#### Manager goals

- Review pending timesheets and resolve them quickly.
- Approve or reject labor submissions with an audit trail.
- Maintain staff records and payroll information.
- Review public enquiries and keep company details current.

#### Admin goals

- Manage site settings and homepage banners.
- Promote users to manager roles.
- Maintain blog and portfolio content through the Django admin interface.

### Scope

#### Included in the project scope

- Public homepage with hero banner, portfolio highlights, company overview, and contact form.
- Portfolio and blog list/detail views with published-only filtering.
- Role-based access for labor staff and managers.
- Temporary password workflow and mandatory password change.
- Timesheet creation, updates, approvals, and payroll reporting.
- Manager dashboard for timesheets, communications, labor records, and payroll exports.
- Admin management for content, banners, and site settings.

#### Outside the initial scope

- Public self-registration.
- Automated email notifications for approvals or replies.
- PDF payroll exports or printable payslips.
- Multi-language support.
- Advanced business analytics or reporting dashboards.

### Structure

The site uses a simple, role-based organisation: public pages, an authenticated labor area, a manager dashboard, and an admin content layer.

- Public navigation: Home, Portfolio, About Us, and Contact Us.
- Labor navigation: timesheet and profile-related options.
- Manager navigation: dashboard tools for review, approvals, labor records, and payroll.
- Admin navigation: Django admin for settings, banners, contact messages, blog content, portfolio content, and profiles.

#### Core database structure

![ERD showing the main BUCON data model](documents/ERD_image.png)

_The data model shows the relationship between user profiles, site settings, portfolio work, blog posts, timesheet records, and dashboard activities._

The main relationships in the project are:

- `Profile` is a one-to-one relationship with the Django `User` model and defines labor and manager roles.
- `SiteSettings` acts as a singleton configuration record for public company details.
- `Banner` stores homepage carousel slides and their display order.
- `ContactMessage` stores public enquiries and their read status.
- `Post` stores blog articles, status, author, and publishing information.
- `Project` stores portfolio entries and `ProjectImage` manages associated gallery images.
- `TimesheetEntry` records labor work, approved status, and payment-related metadata.

### Skeleton (Wireframes)

The design planning for the project was captured in Excalidraw and is stored in the documents folder.

![Home page wireframe](documents/wireframes/Home_page.png)

_Home page wireframe._

![Portfolio list wireframe](documents/wireframes/Portfolio_List.png)

_Portfolio list wireframe._

![Wireframe overview](documents/wireframes/wireframes.svg)

_Overview of the project wireframe set._

![Portfolio detail wireframe](documents/wireframes/Portfolio_detail.png)

_Portfolio detail wireframe._

![Blog list wireframe](documents/wireframes/Blog_List.png)

_Blog list wireframe._

![Blog detail wireframe](documents/wireframes/Blog_Detail.png)

_Blog detail wireframe._

![Timesheets wireframe](documents/wireframes/Timesheets.png)

_Timesheet list and entry workflow wireframe._

![Timesheet add/edit entry wireframe](documents/wireframes/Timesheets_Add&Edit_Entry.png)

_Add/edit timesheet entry wireframe._

![Pending timesheets wireframe](documents/wireframes/Pending_Timesheets.png)

_Pending timesheets approval workflow wireframe._

![All timesheets wireframe](documents/wireframes/All_Timesheets.png)

_All timesheets reporting wireframe._

![Payroll report wireframe](documents/wireframes/Payroll_Report.png)

_Payroll report wireframe._

![Contact messages wireframe](documents/wireframes/Contact_Messages.png)

_Contact message management wireframe._

![Labor account wireframe](documents/wireframes/Add_Labor_Account.png)

_Labor account creation workflow wireframe._

![Dashboard wireframe](documents/wireframes/Dashboard.png)

_Manager dashboard wireframe._

![Staff profile wireframe](documents/wireframes/STAFF_PROFILE.png)

_Staff profile and account-management wireframe._

### Surface

The user interface uses a warm construction-focused palette with earthy tones, strong contrast, and premium styling. The design language reflects a practical, dependable brand image while keeping the experience polished enough for modern digital use. Colour and typography decisions are defined in the main CSS and base template files.

## Design

### Typography

The project uses the fonts declared in the base template and stylesheet:

- **DM Sans** is used for body text, forms, navigation, tables, and interface labels.
- **Libre Baskerville** is used for headings, the company name, and editorial content.

The font pairing creates a professional balance between clean modern UI and a stronger, more established brand presence.

### Colour Scheme

![BUCON colour palette](documents/colors.png)

_The brand palette used throughout the project._

| Colour name           | Hex       | Usage                                |
| --------------------- | --------- | ------------------------------------ |
| `--bucon-ink`         | `#25231F` | Primary text and strong content      |
| `--bucon-ink-soft`    | `#5C574F` | Secondary text and nav labels        |
| `--bucon-walnut`      | `#6B3F2A` | Primary buttons, links, and emphasis |
| `--bucon-walnut-dark` | `#4B2B20` | Headings, dark surfaces, footer      |
| `--bucon-cedar`       | `#B56D45` | Hover states and accent details      |
| `--bucon-brass`       | `#B88A3B` | Highlight accents                    |
| `--bucon-sawdust`     | `#F4EFE6` | Page background                      |
| `--bucon-surface`     | `#FFFDF9` | Cards, panels, tables, and inputs    |
| `--bucon-line`        | `#DED5C8` | Borders and separators               |

### Imagery

The project uses branded company imagery, generated project photography, and product-style media to give the site a clear business identity. The app logo belongs to BUCON, while additional imagery was created to support the portfolio, blog, and homepage presentation. Media is managed through the project’s storage configuration and Cloudinary integration.

## Website Features

### 1. Role-aware navigation and footer

The navigation behaves differently depending on the user role. Visitors see the public menu, while logged-in labor staff and managers receive access to the pages relevant to their responsibilities. The footer content is driven by the project’s singleton site settings record.

![BUCON navbar and footer context](documents/features/change_site_settings.png)

_The site settings model feeds the navbar branding and the footer contact block._

### 2. Homepage with hero carousel, project highlights, and contact form

The homepage brings together the main public-facing elements of the business: a rotating hero banner, featured portfolio work, company information, and a contact form. This creates a clear landing page for both new visitors and returning clients.

![Homepage feature demo](documents/features/home_page_feature.gif)

_Homepage hero carousel and feature sections._

### 3. Portfolio list and detail pages with gallery

The portfolio area shows published projects in an attractive list, and each project has a dedicated detail page with a larger cover image and supporting gallery media. This gives the business a clean way to present examples of its work.

![Portfolio feature demo](documents/features/portfolio.gif)

_Portfolio browsing and detail gallery._

### 4. Blog list and detail pages

The blog makes it easy for BUCON to publish updates, insights, and project news. Only published entries are shown publicly, and each article has a structured detail page for reading and sharing.

![Blog validation screenshot](documents/features/blog_page_feature.png)

_The blog list and published-only logic._

### 5. Contact form with spam protection

The site includes a public enquiry form that accepts a message from a visitor while protecting against automated spam activity. A hidden honeypot field rejects suspicious submissions before they are saved.

![Contact form feature](documents/features/contact_message_feature.png)

_The contact flow and manager message inbox._

### 6. Authentication and access controls

The login flow uses Django Allauth with email-based sign-in and role-aware redirects. Public self-registration is disabled, and the app ensures that sensitive user actions remain protected behind the correct role checks.

![Login page feature](documents/features/Login_page_feature.png)

_The login page and Allauth integration._

### 7. Manager-created labor accounts and password resets

Managers can create labor accounts for staff members and assign temporary passwords when a new employee joins. Password resets are also available when a staff account needs to be reactivated or updated.

![Create labor account demo](documents/features/create_labor_account.gif)

_Manager-side labor account creation flow._

### 8. Forced password-change workflow

New or reset staff accounts are required to choose their own password before continuing to the protected parts of the application. This keeps the system more secure and prevents temporary passwords from being reused.

![Password change form](documents/features/Login_page_feature.png)

_Password-change workflow and login access controls._

### 9. Labor timesheet creation, editing, and history

Labor users can record their shifts, edit entries while they are still pending or rejected, and review their own work history. The timesheet model calculates total working hours automatically to reduce manual errors.

![Timesheet feature GIF](documents/features/all_timesheets_feature.gif)

_Labor timesheet history and management flow._

### 10. Manager approval and rejection workflow

Managers review submitted timesheets and either approve them or reject them with a reason. This gives the business a clear process for validating time records before payroll is prepared.

![Pending timesheets feature](documents/features/pending_timesheets_feature.png)

_Manager queue for pending timesheets._

![Timesheet rejection feature](documents/features/timesheet_rejection_feature.png)

_Rejection workflow with required reason._

### 11. Contact message and labor management

Managers can review public enquiries and maintain labor records, including employment status and hourly rate. This keeps the business operational data organised without exposing it to the public.

![Contact messages dashboard feature](documents/features/contact_message_feature.png)

_Contact message management._

![Dashboard feature overview](documents/features/dashboard_page_feature.png)

_Dashboard overview for contact messages, pending sheets, and account management._

### 12. Payroll reporting with CSV export

The payroll section aggregates approved hours across a selected date range and calculates estimated pay using each worker's hourly rate. Managers can then export the results as a CSV file for further processing.

![Payroll validation screenshot](documents/features/payroll_feature.png)

_Payroll page validation and report layout._

### 13. Admin content management

The admin area provides a central place for managing site settings, homepage banners, blog posts, portfolio items, and user profiles. This allows the business to maintain the website with minimal technical involvement.

![Admin settings screenshot](documents/features/change_site_settings.png)

_Singleton site settings and admin configuration._

### Access control and error handling

The project uses role-based access checks rather than custom page templates for its key permissions. Users with temporary passwords are redirected to change them, manager-only areas are restricted with dedicated mixins, and labor-only views are limited to relevant staff.

## Tablet/Mobile View

![Responsive BUCON view](documents/amiresponsive.png)

_The responsive layout uses Bootstrap 5, a collapsible navbar, and media-query adjustments to ensure the homepage carousel, forms, and tables remain usable on smaller screens._

The responsive behaviour is supported by the Bootstrap grid system and a mobile-focused CSS block that adjusts spacing, image aspect ratios, and layout density for tablet and phone displays.

## Future Features

- Email notifications when a timesheet is approved or rejected.
- PDF payroll exports and printable payslips.
- More advanced time-tracking analytics for labor productivity.
- Portfolio category filtering and search.
- Multi-language support for public pages.
- Worker self-service profile editing and document uploads.
- A dedicated quoting or estimate workflow for construction enquiries.

## Technologies Used

### Languages

| Language   | Version / usage                                                   |
| ---------- | ----------------------------------------------------------------- |
| Python     | 3.12.x environment used in the project and the declared app stack |
| HTML5      | Templates and semantic page structure                             |
| CSS3       | Custom styling in `static/css/main.css`                           |
| JavaScript | Bootstrap carousels and interactive UI behaviour                  |

### Frameworks

| Framework           | Version  | Purpose                                                 |
| ------------------- | -------- | ------------------------------------------------------- |
| Django              | 4.2.30   | Core web framework                                      |
| Bootstrap 5         | 5.3.3    | Layout, forms, tables, cards, and responsive components |
| django-allauth      | 0.57.2   | Authentication and login/logout flow                    |
| django-crispy-forms | 2.1      | Form rendering                                          |
| crispy-bootstrap5   | 2024.2   | Bootstrap 5 form styling                                |
| django-summernote   | 0.8.20.0 | Rich-text editing for content and settings              |
| WhiteNoise          | 6.6.0    | Static file serving in production                       |
| Gunicorn            | 22.0.0   | WSGI app server for Heroku deployment                   |

### Libraries and packages

| Package                   | Version | Purpose                             |
| ------------------------- | ------- | ----------------------------------- |
| cloudinary                | 1.40.0  | Media upload handling               |
| django-cloudinary-storage | 0.3.0   | Cloudinary storage backend          |
| dj-database-url           | 2.2.0   | PostgreSQL connection configuration |
| psycopg2-binary           | 2.9.9   | PostgreSQL database driver          |
| pillow                    | 10.3.0  | Image processing / media support    |
| python-decouple           | 3.8     | Environment variable management     |
| bleach                    | 6.4.0   | Safe HTML sanitisation support      |

### Programs and tools

| Tool                             | Use                                        |
| -------------------------------- | ------------------------------------------ |
| Git                              | Version control                            |
| GitHub                           | Repository hosting and collaboration       |
| Heroku                           | Production deployment platform             |
| PostgreSQL                       | Production database                        |
| Cloudinary                       | Media storage                              |
| dbdiagram.io                     | ERD creation                               |
| Excalidraw                       | Wireframe creation                         |
| VS Code                          | Development environment                    |
| GitHub Copilot                   | AI-assisted coding and README assistance   |
| Claude AI                        | Project planning and user-story generation |
| Gemini                           | Image generation                           |
| Lighthouse                       | Performance and accessibility auditing     |
| W3C HTML/CSS validation services | Front-end validation                       |

## Deployment

The deployment setup reflects the project configuration in the Procfile, Django settings, and dependency list.

1. Create a GitHub repository and push the project code.
2. Create a Heroku app with a unique name and the required region.
3. Create a PostgreSQL database and copy the connection URL into `DATABASE_URL`.
4. Create a Cloudinary account and add the Cloudinary URL to `CLOUDINARY_URL`.
5. Set the required environment variables for the app, including `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` if needed.
6. Ensure the project includes the `Procfile` and required dependencies from `requirements.txt`.
7. Enable WhiteNoise for static assets in production.
8. Connect the GitHub repository to Heroku and deploy the main branch.
9. Run migrations on the deployed application and create a superuser.
10. To run locally, create a virtual environment, install dependencies, set environment variables, apply migrations, and start the app with Django's development server.

## Testing

### Validation

#### HTML validation

The repository includes multiple HTML validation captures in the `documents/html_code_validator/` folder. These screenshots were used to review the structure and confirm that the main pages were built to a clean standard.

![All timesheets HTML validation](documents/html_code_validator/All_timesheet_page_html_test.png)

_All timesheets page HTML validation._

![Blog detail HTML validation](documents/html_code_validator/blog_detail_page_html_test.png)

_Blog detail page HTML validation._

![Blog list HTML validation](documents/html_code_validator/bloglist_page_html_test.png)

_Blog list HTML validation._

![Contact messages HTML validation](documents/html_code_validator/contact_messages_page_html_test.png)

_Contact messages page HTML validation._

![Dashboard HTML validation](documents/html_code_validator/dashboard_page_html_test.png)

_Dashboard page HTML validation._

![Home page HTML validation](documents/html_code_validator/home_page_html_test.png)

_Home page HTML validation._

![Labor accounts HTML validation](documents/html_code_validator/labor_accounts_page_html_test.png)

_Labor accounts page HTML validation._

![Payroll page HTML validation](documents/html_code_validator/payroll_page_html_test.png)

_Payroll page HTML validation._

![Pending timesheets HTML validation](documents/html_code_validator/pending_timesheet_page_html_test.png)

_Pending timesheets HTML validation._

![Portfolio page HTML validation](documents/html_code_validator/portfolio_page_html_test.png)

_Portfolio page HTML validation._

![Project detail HTML validation](documents/html_code_validator/project_page_html_test.png)

_Project detail HTML validation._

![Timesheet HTML validation](documents/html_code_validator/timesheet_page_html_test.png)

_Timesheet page HTML validation._

#### CSS validation

![CSS validator screenshot](documents/css_validator_test.png)

_CSS validation result captured during the front-end checks._

#### JavaScript validation

No dedicated JavaScript file was found in the project assets, so a standalone JavaScript validation step was not required.

#### Python validation by app

##### accounts

| File                                | Result |
| :---------------------------------- | :----: |
| accounts/**init**.py                |   ✅   |
| accounts/adapters.py                |   ✅   |
| accounts/admin.py                   |   ✅   |
| accounts/apps.py                    |   ✅   |
| accounts/forms.py                   |   ✅   |
| accounts/middleware.py              |   ✅   |
| accounts/migrations/0001_initial.py |   ✅   |
| accounts/migrations/**init**.py     |   ✅   |
| accounts/models.py                  |   ✅   |
| accounts/signals.py                 |   ✅   |
| accounts/tests.py                   |   ✅   |
| accounts/urls.py                    |   ✅   |
| accounts/views.py                   |   ✅   |

![Accounts Python validation](documents/python_code_validator/accounts/account_models.png)

_Accounts validation output._

![Accounts form validation](documents/python_code_validator/accounts/account_form.png)

_Account form validation._

![Accounts view validation](documents/python_code_validator/accounts/account_view.png)

_Account view validation._

##### blog

| File                                     | Result |
| :--------------------------------------- | :----: |
| blog/**init**.py                         |   ✅   |
| blog/admin.py                            |   ✅   |
| blog/apps.py                             |   ✅   |
| blog/migrations/0001_initial.py          |   ✅   |
| blog/migrations/0002_post_is_featured.py |   ✅   |
| blog/migrations/**init**.py              |   ✅   |
| blog/models.py                           |   ✅   |
| blog/tests.py                            |   ✅   |
| blog/urls.py                             |   ✅   |
| blog/views.py                            |   ✅   |

![Blog Python validation](documents/python_code_validator/blog/blog_test.png)

_Blog validation output._

![Blog model validation](documents/python_code_validator/blog/blog_models.png)

_Blog model validation._

![Blog view validation](documents/python_code_validator/blog/blog_views.png)

_Blog view validation._

##### core

| File                            | Result |
| :------------------------------ | :----: |
| core/**init**.py                |   ✅   |
| core/admin.py                   |   ✅   |
| core/apps.py                    |   ✅   |
| core/context_processors.py      |   ✅   |
| core/forms.py                   |   ✅   |
| core/migrations/0001_initial.py |   ✅   |
| core/migrations/**init**.py     |   ✅   |
| core/models.py                  |   ✅   |
| core/tests.py                   |   ✅   |
| core/urls.py                    |   ✅   |
| core/views.py                   |   ✅   |

![Core Python validation](documents/python_code_validator/core/core_models.png)

_Core validation output._

![Core admin validation](documents/python_code_validator/core/core_admin.png)

_Core admin validation._

![Core views validation](documents/python_code_validator/core/core_views.png)

_Core views validation._

##### portfolio

| File                                 | Result |
| :----------------------------------- | :----: |
| portfolio/**init**.py                |   ✅   |
| portfolio/admin.py                   |   ✅   |
| portfolio/apps.py                    |   ✅   |
| portfolio/migrations/0001_initial.py |   ✅   |
| portfolio/migrations/**init**.py     |   ✅   |
| portfolio/models.py                  |   ✅   |
| portfolio/tests.py                   |   ✅   |
| portfolio/urls.py                    |   ✅   |
| portfolio/views.py                   |   ✅   |

![Portfolio Python validation](documents/python_code_validator/portfolio/portfolio_models.png)

_Portfolio validation output._

![Portfolio admin validation](documents/python_code_validator/portfolio/portfolio_admin.png)

_Portfolio admin validation._

![Portfolio views validation](documents/python_code_validator/portfolio/portfolio_views.png)

_Portfolio views validation._

##### timesheets

| File                                  | Result |
| :------------------------------------ | :----: |
| timesheets/**init**.py                |   ✅   |
| timesheets/admin.py                   |   ✅   |
| timesheets/apps.py                    |   ✅   |
| timesheets/forms.py                   |   ✅   |
| timesheets/migrations/0001_initial.py |   ✅   |
| timesheets/migrations/**init**.py     |   ✅   |
| timesheets/models.py                  |   ✅   |
| timesheets/tests.py                   |   ✅   |
| timesheets/urls.py                    |   ✅   |
| timesheets/views.py                   |   ✅   |

![Timesheet Python validation](documents/python_code_validator/timesheet/timesheet_models.png)

_Timesheet validation output._

![Timesheet form validation](documents/python_code_validator/timesheet/timesheet_forms.png)

_Timesheet form validation._

![Timesheet view validation](documents/python_code_validator/timesheet/timesheet_views.png)

_Timesheet view validation._

##### dashboard

| File                             | Result |
| :------------------------------- | :----: |
| dashboard/**init**.py            |   ✅   |
| dashboard/admin.py               |   ✅   |
| dashboard/apps.py                |   ✅   |
| dashboard/forms.py               |   ✅   |
| dashboard/migrations/**init**.py |   ✅   |
| dashboard/models.py              |   ✅   |
| dashboard/tests.py               |   ✅   |
| dashboard/urls.py                |   ✅   |
| dashboard/views.py               |   ✅   |

![Dashboard Python validation](documents/python_code_validator/dashboard/dashboard_forms.png)

_Dashboard validation output._

![Dashboard URL validation](documents/python_code_validator/dashboard/dashboard_urls.png)

_Dashboard URLs validation._

![Dashboard view validation](documents/python_code_validator/dashboard/dashboard_views.png)

_Dashboard views validation._

##### config

| File               | Result |
| :----------------- | :----: |
| config/**init**.py |   ✅   |
| config/settings.py |   ✅   |
| config/urls.py     |   ✅   |
| config/wsgi.py     |   ✅   |
| manage.py          |   ✅   |

![Config validation](documents/python_code_validator/config/config_settings.png)

_Configuration validation output._

![Config URL validation](documents/python_code_validator/config/config_urls.png)

_Project configuration URL validation._

#### Lighthouse audits

![Lighthouse audit result](documents/light_house/home_page.png)

_The available Lighthouse capture for the home page._

| Page | Performance                 | Accessibility               | Best Practices              | SEO                         |
| ---- | --------------------------- | --------------------------- | --------------------------- | --------------------------- |
| Home | Available in project report | Available in project report | Available in project report | Available in project report |

#### Browser compatibility and responsiveness

| Area    | Result                                                                              |
| ------- | ----------------------------------------------------------------------------------- |
| Desktop | Bootstrap 5 responsive layout confirmed in the project templates and screenshot set |
| Tablet  | Supported by the responsive layout and multi-device mockup                          |
| Mobile  | Supported by the custom media query at the end of `static/css/main.css`             |

![Multi-device responsive overview](documents/amiresponsive.png)

_Desktop, tablet, and mobile view of the site._

#### Manual testing of user stories

| User Story                             | Test                                                                  | Pass |
| -------------------------------------- | --------------------------------------------------------------------- | ---- |
| Project foundation and role model      | Confirm the app structure and automatic profile creation              | ✅   |
| Shared layout and navigation           | Check that the public and role-based navigation appears correctly     | ✅   |
| Site settings and company details      | Review and update company information from the admin                  | ✅   |
| Homepage banner management             | Create and reorder active hero banners                                | ✅   |
| Home page experience                   | Verify the landing page renders the hero, portfolio, and contact form | ✅   |
| Portfolio browsing                     | Open the portfolio list and detail pages                              | ✅   |
| Blog reading experience                | Open the blog list and read a published article                       | ✅   |
| Contact form for enquiries             | Submit a valid enquiry and confirm it is stored                       | ✅   |
| Manager-led labor account creation     | Create a staff account with a temporary password                      | ✅   |
| Password reset for labor users         | Reset the labor password and confirm forced change is re-enabled      | ✅   |
| Forced password change on first login  | Log in with a temporary password and verify redirection               | ✅   |
| Email-based login                      | Sign in using email and confirm role-based redirect                   | ✅   |
| Daily timesheet submission             | Create a valid timesheet and confirm hour totals are calculated       | ✅   |
| Editing pending or rejected timesheets | Update an in-review timesheet and verify restrictions                 | ✅   |
| Timesheet history                      | Review the labor list and check statuses                              | ✅   |
| Review and approve timesheets          | Approve and reject entries with reasons                               | ✅   |
| Contact message review                 | Open the inbox and mark messages as read                              | ✅   |
| Labor account management               | Update rate and employment status for staff                           | ✅   |
| Payroll reporting                      | Select a date range and review calculated totals                      | ✅   |
| Manager promotion workflow             | Promote a user and verify management access                           | ✅   |
| Blog content management                | Create, publish, and edit blog entries                                | ✅   |
| Portfolio content management           | Add, publish, and manage portfolio projects and galleries             | ✅   |

#### Manual testing of features

| Feature           | Action                             | Expected Result                                           | Status |
| ----------------- | ---------------------------------- | --------------------------------------------------------- | ------ |
| Home page         | Open the landing page              | Hero carousel, featured work, and contact section display | ✅     |
| Navbar            | Login as labor or manager          | Correct role-based menu items appear                      | ✅     |
| Login             | Use the Django Allauth login page  | Successful login redirects to the correct area            | ✅     |
| Contact form      | Submit a valid message             | Message saves and success message appears                 | ✅     |
| Portfolio list    | Open the project list              | Only published projects are shown                         | ✅     |
| Portfolio detail  | Open a project detail              | Full description and gallery load correctly               | ✅     |
| Blog list         | Open published posts               | Only published posts are listed                           | ✅     |
| Timesheet create  | Add a shift                        | Entry saves with the calculated total hours               | ✅     |
| Timesheet edit    | Update a pending or rejected entry | Value updates and rejects reset when needed               | ✅     |
| Timesheet delete  | Delete a pending or rejected entry | Entry is removed successfully                             | ✅     |
| Manager approval  | Approve a pending timesheet        | Status becomes approved and timestamps are set            | ✅     |
| Manager rejection | Reject with reason                 | Status becomes rejected and the reason is stored          | ✅     |
| Payroll report    | Choose date range                  | Totals are aggregated and displayed correctly             | ✅     |
| CSV export        | Click export                       | CSV file downloads correctly                              | ✅     |

#### Automated tests

The project includes Django test coverage across apps. The suite can be run with:

```bash
python manage.py test
```

Verified areas in the repository include:

- `accounts/tests.py` for profile creation, password changes, and login access rules.
- `blog/tests.py` for published-only filtering.
- `portfolio/tests.py` for published project filtering and gallery rendering.
- `timesheets/tests.py` for hours calculation, access restrictions, and deletion rules.
- `dashboard/tests.py` for approval, rejection, and payroll logic.
- `core/tests.py` for singleton settings, banner ordering, and contact-form protections.

#### Bugs addressed

| Issue                                                                                       | Resolution                                                                   | Status   |
| ------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | -------- |
| Temporary passwords could be used beyond the initial login flow.                            | Force-password middleware and redirect logic were added in the accounts app. | ✅ Fixed |
| Spam submissions could reach the contact form through a hidden field.                       | The honeypot field rejects bot submissions before the data is saved.         | ✅ Fixed |
| Invalid times could be submitted with equal start and end times or impossible break values. | Validation in the timesheet form and model logic prevents unsafe totals.     | ✅ Fixed |
| Managers needed a proper way to restrict access to private dashboard features.              | Dedicated manager and labor access mixins enforce the correct role checks.   | ✅ Fixed |

## Credits

The following credit statements reflect the project team's acknowledgements and documentation history:

- Claude AI was used to create the user stories and initial project structure.
- GitHub Copilot was used for bug fixing, README creation, and test support.
- Gemini was used to generate project imagery.
- The BUCON company logo and branding belong to BUCON.
- The ERD was created with https://dbdiagram.io
- The wireframes were created with https://excalidraw.com/
- Special thanks to Marko and Tim for their help and guidance.

### Content references

- Django documentation: https://docs.djangoproject.com/
- django-allauth documentation: https://docs.allauth.org/
- Bootstrap 5 documentation: https://getbootstrap.com/docs/5.3/
- Cloudinary documentation: https://cloudinary.com/documentation
- Python-decouple documentation: https://pypi.org/project/python-decouple/
- WhiteNoise documentation: https://whitenoise.readthedocs.io/
- Code Institute project patterns and guidance informed the project structure and documentation approach.

### Media references

- BUCON company logo and branding: property of BUCON.
- Remaining project imagery in the documents folder was generated with Gemini.
- ERD created with dbdiagram.io.
- Wireframes created with Excalidraw.

### Acknowledgements

Thanks to the BUCON team, the Code Institute team, and the project mentors for the guidance and review that shaped the site and documentation.
