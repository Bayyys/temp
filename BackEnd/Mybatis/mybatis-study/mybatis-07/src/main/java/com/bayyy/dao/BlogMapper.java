package com.bayyy.dao;

import com.bayyy.pojo.Blog;

import java.util.HashMap;
import java.util.List;

public interface BlogMapper {
    // 查询所有博客
    List<Blog> selectAllBlog();

    // 插入博客
    int addBlog(Blog blog);

    // 查询博客
    List<Blog> selectBlogIf(HashMap map);

    // 查询 choose
    List<Blog> selectBlogChoose(HashMap map);

    // 更新 set
    int updateBlogSet(HashMap map);

    // 查询 foreach
    List<Blog> selectBlogForeach(List list);
}
