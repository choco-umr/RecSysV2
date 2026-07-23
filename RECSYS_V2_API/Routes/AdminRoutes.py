from streamlit import error, user

from Schemas.schemas import AdminResearcher_Register_Input,Admin_Register_Input, AdminDeleteUser_Input
from Database.models import Users, Researchers, Admins
from fastapi import Depends, APIRouter, HTTPException, Response, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from Security.security import hash_password, generate_userid, verify_password, create_jwt_token, logout_delete_all_cookies, RBAC
from Database.db import get_db
from Security.exceptions import UserNotAuthorized, UserNotFound

AdminRouter = APIRouter(prefix='/AdminRoutes')

#register admins
@AdminRouter.post("/AdminRegister")
async def AdminRegister(request: Request, User: Admin_Register_Input, db: Session = Depends(get_db)):

    user_type = RBAC(request, db)
    print("user type retunr is", user_type)
    if user_type != "Admin":
        raise UserNotAuthorized()

    DupeUsernameCheck = db.execute(
        select(Admins).where(Admins.USERNAME == User.Username)
    ).scalar_one_or_none()
    
    if DupeUsernameCheck is not None:
        raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )
    else:
        GenerateduserID = generate_userid()
        Hashed_Password = hash_password(User.Password)

        new_user = Admins(
            USER_ID = GenerateduserID,
            USER_TYPE = "Admin",
            FIRST_NAME=User.Firstname,
            LAST_NAME=User.Lastname,
            USERNAME=User.Username,
            PASSWORD=Hashed_Password,
            )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

#register researchers
@AdminRouter.post("/ResearcherRegister")
async def AdminResearcherRegister(request: Request, User: AdminResearcher_Register_Input, db: Session = Depends(get_db)):

    user_type = RBAC(request, db) 
    if user_type != "Admin":
        raise UserNotAuthorized()

    DupeUsernameCheck = db.execute(
        select(Researchers).where(Researchers.USERNAME == User.Username)
    ).scalar_one_or_none()
    
    if DupeUsernameCheck is not None:
        raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )
    else:
        GenerateduserID = generate_userid()
        Hashed_Password = hash_password(User.Password)

        new_user = Researchers(
            USER_ID = GenerateduserID,
            USER_TYPE = "Researcher",
            FIRST_NAME=User.Firstname,
            LAST_NAME=User.Lastname,
            USERNAME=User.Username,
            PASSWORD=Hashed_Password,
            )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

#Delete any user
#register researchers
@AdminRouter.post("/DeleteUser")
async def DeleteUser(request: Request, User: AdminDeleteUser_Input, db: Session = Depends(get_db)):

    user_type = RBAC(request, db) 
    if user_type != "Admins":
        raise UserNotAuthorized()


    user = None
    for table in (Users, Researchers, Admins):
        stmt = select(table).where(table.USERNAME == User.Username)
        found = db.scalars(stmt).first()

        if found:
            user = found
            break

    if not user:
        raise UserNotFound()

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}




#notes
#clean up all htpeceptions
#owast jwt tips for security - https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html