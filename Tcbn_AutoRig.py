# coding=utf-8

import maya.cmds as cmds


class Tcbn_AutoRig:

    # 枝分かれした子を持つジョイントを返す
    def GetBranch(self, joint):
        children = cmds.listRelatives(joint, path=True, type="joint")
        count = len(children)
        if(count == 0):
            return ""
        elif(count >= 2):
            return joint
        else:
            return self.GetBranch(children[0])

    # 末端のジョイントたちを返す
    def GetChildrenEnd(self, joint, _list=[]):
        descendents = cmds.listRelatives(joint, c=True, pa=True, typ="joint")
        if(len(descendents) == 0):
            return _list
        else:
            result = _list
            for child in descendents:
                result += self.GetChildrenEnd(child)
            return result

    # jointから指定したジョイント(root)までの親を返す
    def GetParents(self, root, joint, _list=[]):
        p = cmds.listRelatives(joint, parent=True, pa=True, typ="joint")
        if(len(p) == 0 or p[0] == root):
            return _list
        else:
            _list.insert(0, p)
            return self.GetParents(root, p, _list)

    # あるジョイントの末尾までの長さを数える
    def GetDecendentsCount(self, joint, _l=0):
        children = cmds.listRelatives(joint, path=True, c=True, typ="joint")
        if(len(children) == 0):
            return _l
        else:
            lengths = []
            for c in children:
                lengths += self.GetDecendentsCount(c, _l + 1)
            return max(lengths)

    def SearchBody(self, root):
        self.chest = self.SearchChest(root)
        self.arms = self.SearchArms(self.chest)
        (self.necks, self.haed) = self.SearchHead(self.chest, 1)
        self.legs = self.SearchLegs(root, self.chest)

    # 上胸ボーンを推定する
    def SearchChest(self, root):
        children = cmds.listRelatives(root, path=True, type="joint")
        chest = ""
        chestY = None
        for child in children:
            candidate = self.GetBranch(child)
            if(child == ""):
                continue
            pos = cmds.xform(candidate, q=True, ws=True, t=True)
            if(chestY is None or pos[1] > chestY):
                chestY = pos[1]
                chest = candidate

        return chest

    # 手を推定
    def SearchArms(self, chest):
        children = cmds.listRelatives(
            chest, children=True, path=True, type="joint")
        lengths = []
        for child in children:
            lengths = lengths + (child, self.GetDecendentsCount(child))

        sortedList = sorted(lengths, lambda x: x[1])
        return sortedList[0:2]

    # 頭と首ボーンを推定
    def SearchHead(self, chest, neck_count=1):
        # 末尾の中で最もY座標が高いものを頭の系譜とする
        ends = self.GetChildrenEnd(chest)
        pair = []  # ジョイントとY座標のペア
        for e in ends:
            pos = cmds.xform(e, q=True, ws=True, t=True)
            pair.append(e, pos[1])
        pair.sort(lambda x: x[1])
        _heads_last_pair = pair[-1]
        heads_last = _heads_last_pair[0]
        # 首の数を決めておいて、その手前までを頭とする
        heads_famiry = self.GetParents(chest, heads_last)
        necks = heads_famiry[0: neck_count + 1]
        head = heads_famiry[neck_count]
        return (necks, head)

    # 足を推定
    def SeachLegs(self, root, chest):
        # ルートの子から胸に続く（上半身の）ジョイントを除く
        children = cmds.listRelatives(
            root, children=True, path=True, type="joint")
        chest_root = self.GetParents(root, chest)
        if(chest_root in children):
            children.remove(chest_root)
        # 上半身を除いたルートの子のうち、最も子孫の長い2つを足とする
        lengths = []
        for child in children:
            lengths += (child, self.GetDecendentsCount(child))
        lengths.sort(lambda x: x[1])
        lengths.reverse()
        legs = lengths[0:2]
        return legs
