from math import sqrt
from PIL import Image, ImageDraw
import random
import pprint


def readfile(filename):
    line = [line for line in file(filename)]
    # 1st line is column name, or keyword
    column_name = line[0].strip().split('\t')[1:]
    # Line name or blog name
    line_name = []
    data = []

    for line in line[1:]:
        p = line.strip().split('\t')
        # 1st colunm of each line is blog title, name of that line
        line_name.append(p[0])
        # the rest are data
        data.append([float(x) for x in p[1:]])

    return line_name, column_name, data


def pearson(v1, v2):
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # Sums of the squares
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) *
               (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0:
        return 0

    return 1.0 - num / den


class bigroupe:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance


def groupeh(lines):
    id_current_group = -1
    group = [bigroupe(lines[i], id=i) for i in range(len(lines))]
    while (len(group) > 1):
        # find minimum distance between  2 pair of group to merge
        min_pair = (0, 1)
        d_min = pearson(group[0].vec, group[1].vec)
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                d = pearson(group[i].vec, group[j].vec)
                if d < d_min:
                    d_min = d
                    min_pair = (i, j)
            # Average of 2 groups==> forming new group
        vec_merge = [(group[min_pair[0]].vec[
            i] + group[min_pair[1]].vec[i]) * 0.5
            for i in range(len(group[0].vec))]
        new_group = bigroupe(vec_merge, left=group[min_pair[0]], right=group[
            min_pair[1]], distance=d_min,
            id=id_current_group)

        # After forming new group, id is minus 1 in hierachy tree
        id_current_group -= 1
        # remove original 2 groups which have been merged
        del group[min_pair[1]]
        del group[min_pair[0]]
        group.append(new_group)
        # return when there is only one group left
    return group[0]


def getheight(clust):
    # Is this an endpoint? Then the height is just 1
    if clust.left is None and clust.right is None:
        return 1

    # Otherwise the height is the same of the heights of
    # each branch
    return getheight(clust.left) + getheight(clust.right)


def getdepth(clust):
    # The distance of an endpoint is 0.0
    if clust.left is None and clust.right is None:
        return 0

    # The distance of a branch is the greater of its two sides
    # plus its own distance
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance


def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    # height and width
    h = getheight(clust) * 20
    w = 1200
    depth = getdepth(clust)

    # width is fixed, so scale distances accordingly
    scaling = float(w - 150) / depth

    # Create a new image with a white background
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))

    # Draw the first node
    drawnode(draw, clust, 10, (h / 2), scaling, labels)
    img.save(jpeg, 'JPEG')


def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = getheight(clust.left) * 20
        h2 = getheight(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        # Line length
        ll = clust.distance * scaling
        # Vertical line from this cluster to children
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))

        # Horizontal line to left item
        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))

        # Horizontal line to right item
        draw.line(
            (x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0, 0))

        # Call the function to draw the left and right nodes
        drawnode(draw, clust.left, x + ll, top + h1 / 2, scaling, labels)
        drawnode(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels)
    else:
        # If this is an endpoint, draw the item label
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))


def kclustering(lines, k):
        # fine min/max of each column, that is
        # to say, for each point(word), find min and max
    range_min_max = [(min([line[i] for line in lines]),
                      max([line[i] for line in lines]))
                     for i in range(len(lines[0]))]
    # Each centroid is a vector, with each element placed randomly along the
    # column of data lines
    centroid_group = [[random.random() * (range_min_max[i][1] -
                                          range_min_max[i]
                                          [0]) + range_min_max[i][0]
                       for i in range(len(lines[0]))] for j in range(k)]
    last_match = None
    # Execute 100 times the process to obtain a 'good enough' result
    for step in range(100):
        print 'Step %d executed' % step
        best_match = [[] for i in range(k)]
        centroid_matched = 0

        # find best matched centroid for each line of data
        for i in range(len(lines)):
            d_min = pearson(centroid_group[centroid_matched], lines[i])
            for j in range(k):
                d = pearson(centroid_group[j], lines[i])
                if d < d_min:
                    centroid_matched = j
            best_match[centroid_matched].append(i)
        # if 2 step returns same centroid results=>finish
        if last_match == best_match:
            break
        last_match = best_match

        # Move centroid to new center, which is average of their member
        average_sum = [0.0] * len(lines[0])
        average = [0.0] * len(lines[0])
        for j in range(k):
            if len(best_match[j]) > 0:
                for m in best_match[j]:
                    line_belong_to_centroid = lines[m]
                    for i in range(len(line_belong_to_centroid)):
                        average_sum[i] += line_belong_to_centroid[i]
                average = [x / len(best_match[j]) for x in average_sum]
                centroid_group[j] = average

    return best_match


def start_clustering():
    blogname, words, data = readfile('blogdata.txt')
    groupe = groupeh(data)
    drawdendrogram(groupe, blogname, jpeg='clustering_result.jpg')
    return groupe


def start_kclustering(k):
    blogname, words, data = readfile('blogdata.txt')
    best_matched = kclustering(data, k)
    return best_matched
