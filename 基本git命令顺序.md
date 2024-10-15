# 基本命令

## 可以参考以下执行顺序

- 0.在 sync fork 处获取主仓库的更新
- 1.首先获取远程仓库的修改内容
  使用 git pull <远程仓库的地址> <本地仓库的分支名（默认是 origin 或者 main）>
- 2.查看本地仓库发生的更改
  使用 git status 命令
- 3.选择要提交的内容
  使用 git add <文件名>命令，使用该命令后会将更改添加到队列中
  默认一般使用 git add .命令，会上传所有的更改
- 4.提交更改
  使用 git commit -m "注释" 来提交更改，之后本地仓库存放的内容就保存为更改之后的内容
- 5.将更改提交到远程
  使用 git push <远程仓库的地址> <本地仓库的分支名（默认是 origin 或者 main）> 来将内容提交到 GitHub 之类的远程仓库
- last.将自己的远程仓库同步到所有人的远程仓库。
  在 contribute 处选择 open pull request，检查各个文件的更改，提交更改。

## Author：林一凡，connect with：202130441139@mail.scut.edu.cn

##张瀚到此一游
