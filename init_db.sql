-- 创建数据库
CREATE DATABASE IF NOT EXISTS student_manage DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE student_manage;

-- 创建学生表
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '学号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    age INT DEFAULT 0 COMMENT '年龄',
    gender VARCHAR(10) DEFAULT '' COMMENT '性别',
    major VARCHAR(50) DEFAULT '' COMMENT '专业'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='学生信息表';

-- 插入测试数据
INSERT INTO students (name, age, gender, major) VALUES
('张三', 20, '男', '计算机科学'),
('李四', 21, '女', '软件工程'),
('王五', 19, '男', '数据科学');
