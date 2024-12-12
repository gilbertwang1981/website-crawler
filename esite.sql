CREATE TABLE `fakhruddinsouq_product_scrapy` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `title` varchar(512) NOT NULL DEFAULT '' COMMENT '商品标题',
  `price` varchar(32) NOT NULL DEFAULT '' COMMENT '商品价格',
  `description` varchar(8192) NOT NULL DEFAULT '' COMMENT '商品描述',
  `images` varchar(8192) NOT NULL DEFAULT '' COMMENT '商品图片',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
  `is_deleted` tinyint(4) DEFAULT '0' COMMENT '软删除字段',
  `category` varchar(256) NOT NULL DEFAULT '' COMMENT '类目',
  `spu` varchar(100) NOT NULL DEFAULT '' COMMENT 'spu',
  `sku` varchar(100) NOT NULL DEFAULT '' COMMENT 'sku',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='fakhruddinsouq数据爬虫表';

CREATE TABLE `jubilee_product_scrapy` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `title` varchar(512) NOT NULL DEFAULT '' COMMENT '商品标题',
  `price` varchar(32) NOT NULL DEFAULT '' COMMENT '商品价格',
  `description` varchar(8192) NOT NULL DEFAULT '' COMMENT '商品描述',
  `images` varchar(8192) NOT NULL DEFAULT '' COMMENT '商品图片',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
  `is_deleted` tinyint(4) DEFAULT '0' COMMENT '软删除字段',
  `category` varchar(256) CHARACTER SET utf8mb4 DEFAULT NULL,
  `spu` varchar(100) DEFAULT NULL,
  `sku` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='jubilee数据爬虫表';

CREATE TABLE `saifalfares_product_scrapy` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `title` varchar(512) NOT NULL DEFAULT '' COMMENT '商品标题',
  `price` varchar(32) NOT NULL DEFAULT '' COMMENT '商品价格',
  `description` varchar(8192) NOT NULL DEFAULT '' COMMENT '商品描述',
  `images` varchar(8192) NOT NULL DEFAULT '' COMMENT '商品图片',
  `category` varchar(256) CHARACTER SET utf8mb4 DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
  `is_deleted` tinyint(4) DEFAULT '0' COMMENT '软删除字段',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='saifalfares数据爬虫表';

CREATE TABLE `smartberry_product_scrapy` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `title` varchar(512) NOT NULL DEFAULT '' COMMENT '商品标题',
  `description` varchar(8192) NOT NULL DEFAULT '' COMMENT '商品描述',
  `images` varchar(8192) NOT NULL DEFAULT '' COMMENT '商品图片',
  `category` varchar(256) CHARACTER SET utf8mb4 DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
  `is_deleted` tinyint(4) DEFAULT '0' COMMENT '软删除字段',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='smartberry数据爬虫表';

CREATE TABLE `victorwatch_product_scrapy` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `title` varchar(512) NOT NULL DEFAULT '' COMMENT '商品标题',
  `price` varchar(32) NOT NULL DEFAULT '' COMMENT '商品价格',
  `images` varchar(8192) NOT NULL DEFAULT '' COMMENT '商品图片',
  `category` varchar(256) CHARACTER SET utf8mb4 DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
  `is_deleted` tinyint(4) DEFAULT '0' COMMENT '软删除字段',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='victorwatch数据爬虫表';

CREATE TABLE `hajsabbagh_product_scrapy` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `title` varchar(512) NOT NULL DEFAULT '' COMMENT '商品标题',
  `price` varchar(32) NOT NULL DEFAULT '' COMMENT '商品价格',
  `description` varchar(8192) NOT NULL DEFAULT '' COMMENT '商品描述',
  `images` varchar(8192) NOT NULL DEFAULT '' COMMENT '商品图片',
  `category` varchar(256) CHARACTER SET utf8mb4 DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
  `is_deleted` tinyint(4) DEFAULT '0' COMMENT '软删除字段',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='hajsabbagh数据爬虫表';

CREATE TABLE `salmansaffron_product_scrapy` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '自增id',
  `title` varchar(512) NOT NULL DEFAULT '' COMMENT '商品标题',
  `price` varchar(32) NOT NULL DEFAULT '' COMMENT '商品价格',
  `description` varchar(8192) NOT NULL DEFAULT '' COMMENT '商品描述',
  `images` varchar(8192) NOT NULL DEFAULT '' COMMENT '商品图片',
  `category` varchar(256) CHARACTER SET utf8mb4 DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录最后更新时间',
  `is_deleted` tinyint(4) DEFAULT '0' COMMENT '软删除字段',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='salmansaffron数据爬虫表';