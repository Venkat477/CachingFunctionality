# CachingFunctionality

Its a sample project to create how caching will works internally. In general we will use Redis for caching the records, but inorder to understand how redis work and how it will maintain the records I have created this sample project.

I have used two main functionalities in this caching

***1. LRU Method:*** As caching can't handle too many records in the memory, so this method will clean or delete the records which are least recently used from the cache whenever the cache is full. </br>
***2. TTL Approach:*** Also if for any records where any of the update operations are not required, then those will sit idle in the cache which not required for a cache. So this approach will clear the cache after certian amount of time.

Also all of a sudden if application got crashed,all our caching will get deleted. Inorder to solve this issue, we will write all the caching data in to SSD whenever the cache size crosses 75% and will read whenever the application get restarted.
