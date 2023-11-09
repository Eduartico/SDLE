# Problem

This project aims to build a shopping list application for a large group of users. It must offer offline access, real-time collaboration, and data synchronization between users, presenting challenges in concurrency, data consistency, scalability, and high availability.

**Key Challenges:**

1. **Local-First Shopping Lists:** Users need to create and manage lists on their devices, with offline functionality.

2. **Collaborative Lists:** Users can share lists via unique IDs for concurrent editing by multiple users.

3. **Concurrency and Consistency:** Handling conflicts when multiple users edit a list is crucial. Begin with Last-Writer-Wins and explore CRDTs.

4. **High Availability and Scalability:** Ensure the architecture can scale for a large group of users without data bottlenecks.

5. **Cloud-Based Data Management:** The cloud component provides data storage and synchronization for backup and sharing.


# Architecture

## Link diagram: https://drive.google.com/file/d/1cf-vog9h5PJKpN2sgYrQ8YcekiizRRbt/view (ask permission)

## Link docs: https://docs.google.com/document/d/1z-NKCCy1gVm1qApClmNClSmaLHOZ2kwVCsl1ABZy0FM/edit?usp=sharing

A key element of the project is the architecture of the local-first shopping list application, which establishes the general system architecture and the ways in which the local and cloud components interact to offer a seamless user experience.

### Local Components:

The application's local components, which are installed on user's devices, are essential to its capacity to provide high availability, store data locally, and promote user collaboration. Among these elements are:

* User Interface (UI): The UI allows users to create, view, and amend shopping lists. It is the layer that they can see. Users can maintain their lists, add items, and mark tasks as done through the user interface.

* Local Database: User's devices can keep shopping lists and the things on them in a local database. Users can now access and edit their lists while they're not connected.

* Concurrency management is required to manage possible simultaneous updates of shopping lists by many users. To find the order of actions and settle disputes, the application first uses local clocks and the "Last-Writer-Wins" technique.

![Last-Writer-Wins](diagrams/lww.png)

### Cloud Components:

The cloud's component parts are essential to availability, scalability, and data synchronization among user's devices. These elements consist of:

* Cloud Storage: Users can keep shared shopping lists on a cloud storage platform. With the help of the cloud component, users can access and collaborate on lists since each list is uniquely recognized by an ID, such as a URL.

* Data Replication: Data replication is essential to maintaining shopping list's accessibility and consistency across several platforms. Currently, the program uses "Last-Writer-Wins" to resolve conflicts; however, in the future, Conflict-Free Replicated Data Types (CRDTs) will be implemented to improve conflict resolution.

* Data Sharding: A data sharding approach is used to distribute shopping lists over several servers because each shopping list is independent, and the service is intended to serve millions of customers. This promotes scalability and reduces bottlenecks in data access.

![CRDTs](diagrams/crdt.png)

The architecture of the program is built to support a wide user base, provide high data availability, and facilitate effective user collaboration. Additionally, the design provides the development team with flexibility in selecting the programming languages, frameworks, and technologies that are used to construct the various components, enabling them to make decisions that are optimal for the demands of the project. The structure of the application plays a critical role in guaranteeing that users may reliably and efficiently access the functionalities of the local-first shopping list.

# Pages

Main pages of the application:

| My Account Page| Create New Account | Login Page | 
|---|---|---|
|![My Account](pages/my_account.png) |![Create Account](pages/create_account.png)  | ![Login](pages/login.png)  | 

| Shopping Lists Page | New Shopping List | Shopping List Page|
|---|---|---|
| ![Shopping Lists](pages/shopping_lists.png)| ![New Shopping List](pages/new_list.png)|![Shopping List](pages/shopping_list.png) |

# Features

- Create account and access profile
- Login with email and password
- Create new shopping list
- Add items to shopping list
- Delete items from shopping list
- Mark items as bought
