# RPM相关命令

可以直接使用rpm命令对软件包进行一些操作。

## 安装

```jsx
rpm -ivh <package_name>
rpm -Uvh <package_name> # 没有安装过则安装
rpm -Fvh <package_name> # 没有安装过则忽略
```

-nodeps 忽略

-i install

-v 详细信息

-h 以安装信息栏显示安装进度

—test 可以测试是否有属性依赖

## 卸载

```jsx
rpm -e <package_name> # 有其他包依赖此RPM包时，卸载会报错
```

## 升级

升级时使用-ivh会提示文件冲突

## 查找

rpm -q[licdR]已安装的软件名

rpm -qp[licdR]未安装的文件名称，需要本地有一个未安装的软件包

rpm -qf存在于系统的某个文件名

## 对已安装的包进行文件校验：

```jsx
rpm -V <package_name>
rpm -Vp <rpm_file>
rpm -Va
```

导入key：

rpm - - import <RPM_KEY>

在包安装之前进行签名校验：

rpm -K <rpm_file>

## 重建数据库

RPM数据库存储在/var/lib/rpm内，如果文件损坏，可以重建：

rpm -rebuilddb 解决系统RPM数据库的异常

## YUM命令

yum其实是透明的调用rpm，相当于在rpm基础上封装的更易使用的“前端”。

它主要设计来解决软件包之间的依赖性，并可从多个资源库（源，典型的由/etc/yum.repos.d/目录下的每个.repo文件定义。

## 源制作

createrepo <dir>

一般的CentOS系的ISO镜像中，都带有安装时使用的rpm包。可以将这部分文件的mount到本地，创建本地源，以减少软件安装时的上网下载。

## 安装

```jsx
yum install <package_name>[-<version_info>] -y
yum localinstall <rpm_file>本地安装
yum groupinstall <group_name>组安装
```

## 升级

yum update [package_name]

## 降级

yum downgrade <package_name> - <version_info>

## 卸载

yum remove/erase <package_name>

此命令会卸载掉所有依赖此包的RPM包

## 查找

yum search <packag_name> # 搜索相关软件

yum list # 列出目前yum管理的所有软件，此处包含未安装的软件

yum list以及相关的一些命令能够提供有关软件包、软件包集和软件仓库的信息。所有的yum list命令都能够使用glob表达式作为参数，对输出结果进行过滤。在glob表达式中，可以使用*代表任何数量个字符，使用？代表任何一个字符。

yum list <glob_expr>[more_glob_exprs]列出所有符合glob表达式的软件包

## 本地缓存相关

yum clean all 清除本地缓存

yum makecache只做本地缓存

## yum history

yum history info httpd # info命令查看涉及指定软件包的事务详情

## 依赖包下载研究

利用downloadonly下载，利用这个命令可以一次下载多个包的依赖包的：

利用yumdownloader工具，它可以一次性下载任何RPM软件包及其所有的依赖包。