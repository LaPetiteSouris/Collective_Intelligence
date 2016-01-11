import scipy.stats.pearson as p_s


def readfile(filename):
    line = [line for line in file(filename)]
    # 1st line is column name, or keyword
    column_name = line[0].strip().split('\t')[1:]
    # Line name or blog name
    line_name = []
    data = []

    for line in line[1:]
        p = line.strip().split('\t')
        # 1st colunm of each line is blog title, name of that line
        line_name = append(p[0])
        # the rest are data
        data = append(p[1:])

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
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1))
               * (sum2Sq - pow(sum2, 2) / len(v1)))
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
