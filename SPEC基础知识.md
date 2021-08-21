# SPEC基础知识

## spec文件

制作rpm软件包关键在于编写软件包的spec描述文件。

制作rpm软件包必须写一个软件包描述文件spec。这个文件中包含了软件包的诸多信息，如： 软件包的名字、说明摘要、创建时要执行什么指令、安装时要执行什么操作、以及软件包所要包含的文件列表等等。

实际过程中，最关键的地方是要清楚虚拟路径的位置以及宏的定义。

### 文件头

这个区域定义的Name、Version这些字段对应的值可以在后面通过%{name}, %{version}这样的方式来引用，类似于宏。

- Summary:用一句话概括该软件包尽量多的信息。
- Name：软件包的名字，最终rpm软件包是用该名字与版本号（Version）、释出号（Release）及体系号来命名软件包的，后面可使用%{name}的方式引用
- Version:软件版本号。仅当软件包比以前有较大改变时才增加版本号，后面可使用%{version}引用
- Release：软件包释出号/发行号。一般我们对该软件包做了一些小的补丁的时候就应该把释出号加1，后面可使用%{release}引用
- Packager：打包的人（一般是个人邮箱）
- Vendor：软件开发者的名字，发行商或打包组织的信息。
- License：软件授权方式，通常是GPL（自由软件）或GPLv2，BSD
- Copyright：软件包所采用的版权规则。
- Group：软件包所属类别
    - Development/System （开发/系统）
    - System Environment/Daemons（系统环境/守护）
- Source：源程序软件包的名字/源代码包的名字，如stardict-2.0.tar.gz。可以带多个用Source1、Source2等源，也可以用%{source1}、%{source2}引用
- BuildRequires：制作过程中用到的软件包，构建依赖
- Requires:安装时所需软件包
    - Requires（pre）：指定不同阶段的依赖
- BuildRoot：安装或编译时使用的虚拟目录，打包时会用到该目录下文件，可查看安装后文件路径，例如：BuildRoot: %_topdir/BUILDROOT。
- Prefix:%{_prefix}为了解决今后安装rpm包时，不一定把软件安装到rpm中打包的目录的情况。必须在这里定义该标识，并在编写%install脚本的时候引用，实现rpm安装时重新指定位置的功能。
- BuildArch：指编译的目标处理器结构，noarch标识不指定，但通常都是以/usr/lib/rpm/marcos中的内容为默认值
- %description：软件包详细说明，可写在多个行上。任何人使用rpm -qi查询软件包时都可以看到。可以解释软件包做什么，描述任何警告或附加的配置指令
- URL：软件的主页

#查看头部信息和查看脚本内容

![SPEC%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86%20da3d788f4abd464cb55b645dc0742ceb/Untitled.png](SPEC%E5%9F%BA%E7%A1%80%E7%9F%A5%E8%AF%86%20da3d788f4abd464cb55b645dc0742ceb/Untitled.png)

## RPM包依赖

依赖关系定义了一个包正常工作需要依赖的其他包，RPM在升级、安装和删除的时候会确保依赖关系得到满足。

## BuildRequires

定义构建时依赖的软件包，在构建机器编译rpm包时需要的辅助工具，以逗号分隔。

## Requires

定义安装时的依赖包，该rpm包所依赖的软件包名称，指编译好的rpm软件在其他机器上安装时，需要依赖的其他软件包。

## BuildRoot

在生成rpm的过程中，执行make install时会把软件安装到上述的路径中，在打包的时候，同样依赖“虚拟目录”为“根目录”进行操作。可使用$RPM_BUILD_ROOT方式引用。

spec脚本主体：

## %prep阶段

预处理，通常用来执行一些解开源程序包的命令，为下一步的编译安装作准备。

%prep和下面的%build, %install段一样，除了可以执行rpm所定义的宏命令以外，还可以执行SHELL命令，可以有很多行，如常写的tar解包命令。功能上类似于./configure。

%prep阶段进行实际的打包准备工作，是使用节前缀%prep表示的。主要功能有：

将文件SOURCES/解压到构建目录BUILD/

应用Patch（打补丁）（SOURCES/ ⇒ BUILD/)

描述rm -rf $RPM_BUILD_ROOT

描述或编辑本部分用到的命令到PreReq

通过-b .XXX描述补丁备份

一般包含%setup与%patch两个命令。%setup用于将软件包打开，执行%patch可将补丁文件加入解开的源程序中。

## %setup

这个宏解压源代码，将当前目录改为源代码解压之后产生的目录。

主要的用途是将%sourcedir目录下的源代码解压到%builddir目录下，将~/rpmbuild/SOURCES里的包解压到~/rpmbuild/BUILD/%{name}-%{version}中。

应该 -q 参数给 %setup 宏。这会显著减少编译日志文件的输出，尤其是源代码包会解压出一堆文件的时候。

## %patch

这个宏将头部定义的补丁应用于源代码。通常补丁都会一起在源码tar.gz包中，或放到SOURCES目录下。

## %build阶段

本段时构建阶段，会在%_builddir目录下执行源码包的编译。执行常见的configure和make操作。该阶段一般由多个make命令组成。于%prep段落一样，这些命令可以是shell命令，也可以是宏。

%build和%install过程中，都必须把编译和安装的文件定义到虚拟根目录中

%file中用的是相对目录

%configure是rpm定义的标准宏命令。执行源代码的configure配置。会自动将prefix设置成/usr。

## %install 阶段

安装阶段就是执行make install命令操作。开始把软件安装到虚拟的根目录中。这个阶段会在%buildrootdir目录里建好目录结构，然后将需要打包到rpm软件包里的文件从%builddir里拷贝到%_buildrootdir里对应的目录里。

在~/rpmbuild/BUILD/%{name}-%{version}目录中进行make install很重要，如果路径不对，则下面%file中寻找文件的时候就会失败。

## %files阶段（该字段应是主要检测的部分）

文件段，主要用来说明会将%{buildroot}目录下的哪些文件和目录最终打包到rpm包里。定义软件包所包含的文件，分为三类：

- 说明文档（doc）
- 配置文件（config）
- 执行程序

还可定义文件存取权限，拥有者及组别。

会在虚拟根目录下进行，应用宏或变量表示相对路径。

在%files阶段的第一条命令的语法是：

%defattr（文件权限，用户名，组名，目录权限）

%files
%defattr (-,root,root,0755)                         ← 设定默认权限
%config(noreplace) /etc/my.cnf                      ← 表明是配置文件，noplace表示替换文件
%doc %{src_dir}/Docs/ChangeLog                      ← 表明这个是文档
%attr(644, root, root) %{_mandir}/man8/mysqld.8*    ← 分别是权限，属主，属组
%attr(755, root, root) %{_sbindir}/mysqld

%exclude列出不想打包到rpm中的文件。

在安装rpm时，会将可执行的二进制文件放在/usr/bin目录下，动态库放在/usr/lib或者/usr/lib64目录下，配置文件放在/etc目录下，并且多次安装时新的配置文件不会覆盖已经存在的同名配置文件。

%files阶段有两个特性：

%{buildroot}里的所有文件都要明确被指定是否要被打包到rpm里。假如，%{buildroot} 目录下有 4 个目录 a、b、c和d，在 %files 里仅指定 a 和 b 要打包到 rpm 里，如果不把 c 和 d 用 exclude 声明是要报错的；

如果声明了 %{buildroot} 里不存在的文件或者目录也会报错。

关于 %doc 宏，所有跟在这个宏后面的文件都来自 %{_builddir} 目录，当用户安装 rpm 时，由这个宏所指定的文件都会安装到 /usr/share/doc/name-version/ 目录里。

## %clean

清理段，通过—clean删除BUILD

编译完成后一些清理工作，主要包括对%{buildroot}目录的清空，通常执行注入make clean之类的命令。

## %changelog

修改日志段，记录spec的修改日志段。将软件的每次修改记录到这里，保存到发布的软件包中，以便查询用。

## 宏

在定义文件的安装路径时，通常会使用类似%_sharedstatedir的宏。

RPM 内建宏定义在 `/usr/lib/rpm/redhat/macros` 文件中，这些宏基本上定义了目录路径或体系结构等等；同时也包含了一组用于调试 spec 文件的宏。

所有宏都可以在 `/usr/lib/rpm/macros` 找到。

利用 rpmbuild 构建 rpm 安装包时，通过命令 `rpm --showrc|grep prefix` 查看。

通过 `rpm --eval "%{macro}"` 来查看具体对应路径。

比如我们要查看 `%{_bindir}` 的路径，就可以使用命令 `rpm --eval "%{ _bindir}"` 来查看。

## 变量

define定义的变量类似于局部变量，只在%{!?foo: ... }区间有效，不过SPEC不会自动清除该变量，只有再次遇到%{}时才会清除。

- `define` 用来定义宏，`global` 用来定义变量；
- 如果定义带参数的宏 (类似于函数)，必须要使用 `define`；
- 在 `%{}` 内部，必须要使用 `global` 而非 `define`；
- `define` 在使用时计算其值，而 `global` 则在定义时就计算其值；