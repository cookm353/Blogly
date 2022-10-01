## Part One

### Create User Model

| User | Details |
|-|-|
| id | primary key |
| first_name | text |
| last_name | text |
| img_url | text |

### Create Flask app

- Make a basic Flask app
- Can match the one from the lectures
- Should import the **User** model and create tables w/ SQLAlchemy

### Make a Base Template

- Make the base template, then add templates for the other routes
- Don't worry about styling too much

### Make Routes for Users

- [x] GET /
  - Redirect to list of users
- [x] GET /users
  - Show all users
  - Make links to view detail page for the user
  - Have link to add-user form
- [x] GET /users/new
  - Show add form for users
- [x] POST /users/news
  - Process the add form, adding a new user and returning to /users
- [x] GET /users/[user-id]
  - Show info about specified user
  - Have button to edit page or delete user
- [x] GET /users/[user-id]/edit
  - Edit page for user
  - Have a cancel button that returns to detail page and save button to update user
- [x] POST /users/[user-id]/edit
  - Process edit form and return user to /users
- [x] POST /users/[user-id]/delete
  - Delete user

### Testing

- Make sure there are tests for at least 4 of the routes

### Further Study

#### Full Name Method

- Implement a full name method and edit routes to use this instead for first_name and last_name

#### Turn Full Name into a Property

- Look up how to make a Python property on a class
- Class properties are used like attributes, but are actually methods

## Part Two

### Post Model

- Make another model for blog posts

| Column | Details |
|-| - |
|**id**|Primary key|
|title|Text|
|content|Text|
|created_at|Date-time|
|user_id|Foreign key|

### UI

- [ ] Add list of posts to user detail page
- [ ] Add 'Add Post' button below list of posts
- [ ] Implement a new post form
- [ ] Create another page for new post form
- [ ] Create a page for displaying posts
- [ ] Create post edit form

### New Routes

- [ ] GET /users/[user-id]/posts/new
- [ ] POST /users/[user-id]/posts/new
- [ ] GET /posts/[post-id]
- [ ] GET /posts/[post-id]/edit
- [ ] POST /posts/[post-id]/edit
- [ ] POST /posts/[post-id]/delete

### Other tasks

- [ ] Change user page to show posts for user
- [ ] Update broken tests and implement new ones

## Further Study

- [ ] Make the homepage display the 5 most recent posts
- [ ] When listing posts, use a more readable format
- [ ] Add a custom 404 error page (requires research)
- [ ] Cascade deletion of user - when a user is deleted their posts should automatically be deleted also