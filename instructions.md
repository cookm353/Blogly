# Part One

## Create User Model

| User | Details |
|-|-|
| id | primary key |
| first_name | text |
| last_name | text |
| img_url | text |

## Create Flask app

- Make a basic Flask app
- Can match the one from the lectures
- Should import the **User** model and create tables w/ SQLAlchemy

## Make a Base Template

- Make the base template, then add templates for the other routes
- Don't worry about styling too much

## Make Routes for Users

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
- [ ] POST /users/[user-id]/edit
  - Process edit form and return user to /users
- [x] POST /users/[user-id]/delete
  - Delete user

## Testing

- Make sure there are tests for at least 4 of the routes

## To-Do

- Fix editing user (collecting arguments and passing to model)
- Implement more tests!

## Further Study

### Full Name Method

- Implement a full name method and edit routes to use this instead for first_name and last_name

### List Users in Order

- List users in alphabetical order by last name
- You can just get SQLAlchemy to do this

### Turn Full Name into a Property

- Look up how to make a Python property on a class
- Class properties are used like attributes, but are actually methods
