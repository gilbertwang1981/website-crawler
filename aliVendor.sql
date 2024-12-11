CREATE TABLE `product_vendor_1688` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `offer_id` varchar(32) NOT NULL DEFAULT '' COMMENT '商品的offerId',
  `mobile` varchar(32) NOT NULL DEFAULT '' COMMENT '手机号',
  `title` varchar(256) NOT NULL DEFAULT '' COMMENT '商品标题',
  `company` varchar(128) NOT NULL DEFAULT '' COMMENT '公司',
  `category_one` varchar(64) NOT NULL DEFAULT '' COMMENT '一级分类',
  `category_two` varchar(64) NOT NULL DEFAULT '' COMMENT '二级分类',
  `category_three` varchar(64) NOT NULL DEFAULT '' COMMENT '三级分类',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
  `is_deleted` tinyint(4) DEFAULT '0' COMMENT '软删除字段',
  PRIMARY KEY (`id`),
  UNIQUE KEY `product_vendor_1688_offerId_IDX` (`offer_id`) USING BTREE,
  KEY `product_vendor_1688_category_one_IDX` (`category_one`,`category_two`,`category_three`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=473 DEFAULT CHARSET=utf8 COMMENT='商品供应商表';
