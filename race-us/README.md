# README

Paper: [Toward a Programmable Humanizing Artificial Intelligence Through Scalable Stance-Directed Architecture](https://ieeexplore.ieee.org/abstract/document/10659024)

### Files

- **lv1_users.csv** – Mapping of user_ids to level-1 communities.  
- **lv2_users.csv** – Mapping of user_ids to level-2 communities.  
- **lv2_labels.png** – Camp labels for level-2 communities.  
- **sorted_narratives_alm.json** – Patterned top narratives for ALM.  
- **sorted_narratives_blm.json** – Patterned top narratives for BLM.  

### Community Detection

- Communities obtained using the **Louvain algorithm** on a retweet network.  
- User IDs converted from float values to integers.
- Network edges were constructed between `user_id` and `parent_user_id`, with an **edge threshold of 2**. 
- Edges and nodes prepared for **Gephi** to run and visualize top communities.  
- Each top-level community was re-run as a **new network** in Gephi to obtain its **level-2 communities**, by preparing new nodes and edges files from the users in that community and running community detection again.  
