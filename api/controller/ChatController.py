from api.controller.UserController import UserController
from api.schema.UserSchema import UserToken
from helper.database import chat_collection, user_collection, chat_user_collection

def contact_helper(contact) -> dict:
    return {
        "id": str(contact["_id"]),
        "created_by": contact["created_by"],
        "user_id": contact["user_id"],
        "is_group": contact["is_group"],
        "name": contact["name"],
        "created_at": contact["created_at"]
    }

class ChatController:
    @staticmethod
    async def get_chats(user: UserToken):
        or_query = {
            "$or": [
                {"created_by": user.get("id")},
                {"user_id": user.get("id")}
            ]
        }
        contacts = await chat_user_collection.find(or_query).to_list(100)
        if not contacts:
            html_contacts = "No contacts found"
        else:
            html_contacts = ""
            for contact in contacts:
                if contact["created_by"] == user.get("id"):
                    contact_name = await user_collection.find_one({"_id": contact["user_id"]})["name"]
                else:
                    contact_name = await user_collection.find_one({"_id": contact["created_by"]})["name"]
                html_contacts += f"""
                    <li>
                        <a onclick="openChat({contact['id']})" style="cursor: pointer">
                            <div class="d-flex align-items-start">
                                <div class="flex-shrink-0 me-3 align-self-center">
                                    <div class="user-img online">
                                        <div class="avatar-xs align-self-center">
                                            <span
                                                class="avatar-title rounded-circle bg-primary-subtle text-primary">
                                                {contact_name[0]}
                                            </span>
                                        </div>
                                        <span class="user-status"></span>
                                    </div>
                                </div>

                                <div class="flex-grow-1 overflow-hidden">
                                    <h5 class="text-truncate font-size-14 mb-1">
                                       {contact_name}
                                    </h5>
                                    <p class="text-truncate mb-0">
                                        Hello
                                    </p>
                                </div>

                                <div class="flex-shrink-0">
                                    <div class="font-size-11">02 min</div>
                                </div>
                            </div>
                        </a>
                    </li>
                """
                
        html_sidebar = f"""
            <div class="d-lg-flex mb-4" style="height: 100vh; overflow: hidden">
                <div class="chat-leftsidebar card" style="height: 100vh !important">
                    <div class="p-3 px-4">
                        <div class="d-flex align-items-start">
                            <div class="flex-shrink-0 me-3 align-self-center">
                               
                            </div>

                            <div class="flex-grow-1">
                                <h5 class="font-size-16 mb-1">
                                    <a href="#" class="text-reset">{user.get("name")}
                                        <i class="mdi mdi-circle text-success align-middle font-size-10 ms-1"></i></a>
                                </h5>
                                <p class="text-muted mb-0">Available</p>
                            </div>

                            <div class="flex-shrink-0">
                                <div class="dropdown chat-noti-dropdown">
                                    <button class="btn dropdown-toggle py-0" type="button" data-bs-toggle="dropdown"
                                        aria-haspopup="true" aria-expanded="false">
                                        <i class="uil uil-ellipsis-h"></i>
                                    </button>
                                    <div class="dropdown-menu dropdown-menu-end">
                                        <a class="dropdown-item" href="#" data-bs-toggle="modal"
                                            data-bs-target="#profileModal">Profile</a>
                                        <a class="dropdown-item" href="#">Edit</a>
                                        <a class="dropdown-item" href="#">Add Contact</a>
                                        <a class="dropdown-item" href="#">Setting</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="p-3">
                        <div class="search-box chat-search-box">
                            <div class="position-relative">
                                <input type="text" class="form-control bg-light border-light rounded" placeholder="Search..." />
                                <i class="uil uil-search search-icon"></i>
                            </div>
                        </div>
                    </div>

                    <div class="pb-3 h-100 overflow-auto">
                        <div class="chat-message-list" data-simplebar style="height: 100vh !important">
                            <div class="p-4 border-top">
                                <div>
                                    <div class="float-end">
                                        <a href="javascript:void(0);" class="text-primary"><i class="mdi mdi-plus"></i> New
                                            Group</a>
                                    </div>
                                    <h5 class="font-size-16 mb-3">
                                        <i class="uil uil-users-alt me-1"></i> Groups
                                    </h5>

                                    <ul class="list-unstyled chat-list group-list">
                                        
                                    </ul>
                                </div>
                            </div>

                            <div class="p-4 border-top">
                                <div>
                                    <div class="float-end">
                                        <a href="" class="text-primary" data-bs-toggle="modal"
                                            data-bs-target="#addContactModal"><i class="mdi mdi-plus"></i> New
                                            Contact</a>
                                    </div>
                                    <h5 class="font-size-16 mb-3">
                                        <i class="uil uil-user me-1"></i> Contacts
                                    </h5>

                                    <ul class="list-unstyled chat-list">
                                        {html_contacts}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- end chat-leftsidebar -->

                <div class="w-100 user-chat mt-4 mt-sm-0 ms-lg-1" id="chat-content">

                </div>
            </div>
        """
        
        # Get all users 
        users = await UserController.get_users(user)
        html_chats = ""
        for item in users:
            html_chats += f"""
                <li>
                    <a href="#" onclick="addContact('{item.get('id')}')">
                        <div class="d-flex align-items-start">
                            <div class="flex-shrink-0 me-3 align-self-center">
                                <div class="user-img online">
                                    <div class="avatar-xs align-self-center">
                                        <span
                                            class="avatar-title rounded-circle bg-primary-subtle text-primary">
                                            {item.get('name')[0]}
                                        </span>
                                    </div>
                                    <span class="user-status"></span>
                                </div>
                            </div>

                            <div class="flex-grow-1 overflow-hidden">
                                <h5 class="text-truncate font-size-14 mb-1">
                                    {item.get('name')}
                                </h5>
                                <p class="text-truncate text-body mb-0">
                                    {item.get('email')} | {item.get('phone')}
                                </p>
                            </div>
                            <div class="flex-shrink-0">
                                <div class="font-size-11">02 min</div>
                            </div>
                        </div>
                    </a>
                </li>
            """
        return {
            "html_sidebar": html_sidebar,
            "html_chats": html_chats
        }
    
    @staticmethod
    async def add_contact(contact: str, user: UserToken):
        or_query = {
            "$or": [
                {"created_by": user.get("id")},
                {"created_by": contact},
                {"user_id": user.get("id")},
                {"user_id": contact}
            ]
        }
        contacts = await chat_user_collection.find_one(or_query)
        if not contacts:
            chat_user = {
                "created_by": user.get("id"),
                "user_id": contact
            }
            return await chat_user_collection.insert_one(chat_user)
        
    