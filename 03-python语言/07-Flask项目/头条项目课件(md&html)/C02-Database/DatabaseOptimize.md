# 数据库理论--数据库优化

> 数据库是Web应用至关重要的一个环节，其性能的优劣会影响整合Web应用，所以需要对数据库进化优化以提高使用性能。以下提供几点方法作为参考。

[TOC]

<!-- toc -->

## 1 理解索引

> ![数据库索引](../images/数据库索引.png)
>
> 
>
> - 索引本质就是又建立一张表（各种B树结构），表中存储了索引字段的值和该值数据所在的位置，方便快速查找
> - 重要结论：
>   - 索引会提升查速度，降低写（增删改）的速度
>   - 如果不做读写分离，只对`经常性只读的数据字段`设置索引，又读又写的字段不设置索引

## 2 SQL查询优化

> - 避免全表扫描，应考虑在 where 及 order by 涉及的列上建立索引；
>
> - 查询时使用select明确指明所要查询的字段，避免使用`select *`的操作；
>
> - SQL语句尽量大写，如
>
>   ```sql
>   SELECT name FROM t WHERE id=1
>   ```
>
>   对于小写的sql语句，通常数据库在解析sql语句时，通常会先转换成大写再执行。
>
> - 尽量避免在 where 子句中使用!=或<>操作符， MySQL只有对以下操作符才使用索引：<，<=，=，>，>=，BETWEEN，IN，以及某些时候的LIKE；
>
>   ```sql
>   SELECT id FROM t WHERE name LIKE ‘abc%’ 
>   ```
>
> - 对于模糊查询，如：
>
>   ```sql
>   SELECT id FROM t WHERE name LIKE ‘%abc%’ 
>   ```
>
>   或者
>
>   ```sql
>   SELECT id FROM t WHERE name LIKE ‘%abc’
>   ```
>
>   将导致全表扫描，应避免使用，若要提高效率，可以考虑全文检索；
>
> - 遵循最左原则，在where子句中写查询条件时把索引字段放在前面，如
>
>   ```sql
>   mobile为索引字段，name为非索引字段
>   推荐
>   SELECT ... FROM t WHERE mobile='13911111111' AND name='python'
>   不推荐
>   SELECT ... FROM t WHERE name='python' AND mobile='13911111111' 
>   
>   建立了复合索引 key(a, b, c)
>   推荐
>   SELECT ... FROM t WHERE a=... AND b=... AND c= ...
>   SELECT ... FROM t WHERE a=... AND b=...
>   SELECT ... FROM t WHERE a=...
>   不推荐 (字段出现顺序不符合索引建立的顺序)
>   SELECT ... FROM t WHERE b=... AND c=...
>   SELECT ... FROM t WHERE b=... AND a=... AND c=...
>   ...
>   ```
>
> - 能使用关联查询解决的尽量不要使用子查询，如
>
>   ```sql
>   子查询
>   SELECT article_id, title FROM t_article WHERE user_id IN (SELECT user_id FROM t_user  WHERE user_name IN ('itcast', 'itheima', 'python'))
>   
>   关联查询(推荐)
>   SELECT b.article_id, b.title From t_user AS a INNER JOIN t_article AS b ON a.user_id=b.user_id WHERE a.user_name IN ('itcast', 'itheima', 'python');
>   ```
>
>   能不使用关联查询的尽量不要使用关联查询；
>
> - 不需要获取全表数据的时候，不要查询全表数据，使用LIMIT来限制数据。
>
> - MySQL提供的一种日志记录，用来记录在MySQL中**响应时间超过阀值**的语句，全名是**慢查询日志**，简称[**MySQL的慢查询**](https://blog.csdn.net/qq_40884473/article/details/89455740)，可以通过该日志定位查询问题后，按上述方法进行查询优化

## 3 数据库优化

> - 在进行表设计时，可适度增加冗余字段(反范式设计)，减少JOIN操作；
> - 多字段表可以进行垂直分表优化，多数据表可以进行水平分表优化；
> - 选择恰当的数据类型，如整型的选择；
> - 对于强调快速读取的操作，可以考虑使用MyISAM数据库引擎；
> - 对较频繁的作为查询条件的字段创建索引；唯一性太差的字段不适合单独创建索引，即使频繁作为查询条件；更新非常频繁的字段不适合创建索引；
> - 编写SQL时使用上面的方式对SQL语句进行优化；
> - 使用慢查询工具找出效率低下的SQL语句进行优化；
> - 构建缓存，减少数据库磁盘操作；
> - 可以考虑结合使用内在型数据库，如Redis，进行混合存储。