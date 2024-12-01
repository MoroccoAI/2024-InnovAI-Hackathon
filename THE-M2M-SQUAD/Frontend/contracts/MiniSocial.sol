// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

contract CoolSocialContract {

    uint public coolNumber = 10; // Keeping the original coolNumber functionality

    struct Post {
        string message;
        address author;
        uint256 timestamp;
        uint256 lastModified;
        uint256 likes;
        uint256 dislikes;
    }

    Post[] public posts;

    event PostPublished(uint postId, address author, string message, uint256 timestamp);
    event PostLiked(uint postId, address user, uint256 likes);
    event PostDisliked(uint postId, address user, uint256 dislikes);
    event PostModified(uint postId, string newMessage, uint256 lastModified);

    function setCoolNumber(uint _coolNumber) public {
        coolNumber = _coolNumber;
    }

    function publishPost(string memory _message) public {
        uint256 postId = posts.length;
        Post memory newPost = Post({
            message: _message,
            author: msg.sender,
            timestamp: block.timestamp,
            lastModified: 0,
            likes: 0,
            dislikes: 0
        });
        posts.push(newPost);
        emit PostPublished(postId, msg.sender, _message, block.timestamp);
    }

    function getPost(uint index) public view returns (
        string memory, 
        address, 
        uint256, 
        uint256, 
        uint256, 
        uint256
    ) {
        require(index < posts.length, "Index out of bounds");
        Post memory post = posts[index];
        return (post.message, post.author, post.timestamp, post.lastModified, post.likes, post.dislikes);
    }

    function getTotalPosts() public view returns (uint) {
        return posts.length;
    }

    function likePost(uint index) public {
        require(index < posts.length, "Index out of bounds");
        posts[index].likes += 1;
        emit PostLiked(index, msg.sender, posts[index].likes);
    }

    function dislikePost(uint index) public {
        require(index < posts.length, "Index out of bounds");
        posts[index].dislikes += 1;
        emit PostDisliked(index, msg.sender, posts[index].dislikes);
    }

    function editPost(uint index, string memory newMessage) public {
        require(index < posts.length, "Index out of bounds");
        Post storage post = posts[index];
        require(msg.sender == post.author, "Only the author can edit the post");

        post.message = newMessage;
        post.lastModified = block.timestamp;
        emit PostModified(index, newMessage, post.lastModified);
    }
}
