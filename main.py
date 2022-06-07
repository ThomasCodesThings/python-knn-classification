import random
import math
import matplotlib.pyplot as plt
import datetime

class Point:
    x = 0
    y = 0
    color = None

    def calculateDistance(self, secondPoint):
        d = math.pow((secondPoint.x - self.x), 2.0) + math.pow((secondPoint.y - self.y), 2.0)
        return math.sqrt(d)

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

class Classification:

    point_list = []
    generated_points_dict = {
        'red': [],
        'red_all': [],
        'green': [],
        'green_all': [],
        'blue': [],
        'blue_all': [],
        'purple': [],
        'purple_all': []
    }
    plot_points_list = []

    def generate_random_point(self, key, start_x, end_x, start_y, end_y, color):
        p_x = random.randint(start_x, end_x)
        p_y = random.randint(start_y, end_y)
        p = Point(p_x, p_y, color)
        while(p in self.generated_points_dict[key]):
            p_x = random.randint(start_x, end_x)
            p_y = random.randint(start_y, end_y)
            p = Point(p_x, p_y, color)

        self.generated_points_dict[key].append(p)

    def init(self):
        pr_1 = Point(-4500, -4400, 'red')
        pr_2 = Point(-4100, -3000, 'red')
        pr_3 = Point(-1800, -2400, 'red')
        pr_4 = Point(-2500, -3400, 'red')
        pr_5 = Point(-2000, -1400, 'red')

        pg_1 = Point(4500, -4400, 'green')
        pg_2 = Point(4100, -3000, 'green')
        pg_3 = Point(1800, -2400, 'green')
        pg_4 = Point(500, -3400, 'green')
        pg_5 = Point(2000, -1400, 'green')

        pb_1 = Point(-4500, 4400, 'blue')
        pb_2 = Point(-4100, 3000, 'blue')
        pb_3 = Point(-1800, 2400, 'blue')
        pb_4 = Point(-2500, 3400, 'blue')
        pb_5 = Point(-2000, 1400, 'blue')

        pp_1 = Point(4500, 4400, 'purple')
        pp_2 = Point(4100, 3000, 'purple')
        pp_3 = Point(1800, 2400, 'purple')
        pp_4 = Point(2500, 3400, 'purple')
        pp_5 = Point(2000, 1400, 'purple')

        self.init_points = [pr_1, pr_2, pr_3, pr_4, pr_5, pg_1, pg_2, pg_3, pg_4, pg_5, pb_1, pb_2, pb_3, pb_4, pb_5, pp_1, pp_2, pp_3, pp_4, pp_5]

    def normal_generate(self):
        if(random.randint(1, 100) < 100):
            return True
        return False

    def generate_points(self):
        for i in range(0, self.points_to_generate//4):
            self.generate_random_point('red', -5000, 499, -5000, 499, 'red')
            self.generate_random_point('red_all', -5000, 5000, -5000, 5000, 'red')
            self.generate_random_point('green', -499, 5000, -5000, 499, 'green')
            self.generate_random_point('green_all', -5000, 5000, -5000, 5000, 'green')
            self.generate_random_point('blue', -5000, 499, -499, 5000, 'blue')
            self.generate_random_point('blue_all', -5000, 5000, -5000, 5000, 'blue')
            self.generate_random_point('purple', -499, 5000, -499, 5000, 'purple')
            self.generate_random_point('purple_all', -5000, 5000, -5000, 5000, 'purple')


    def classify(self, point, k):
        color_dict = {
            'red': 0,
            'green': 0,
            'blue': 0,
            'purple': 0
        }

        closest_neighbours = sorted(self.point_list, key=lambda p: point.calculateDistance(p))[1:k+1]

        for p in closest_neighbours:
            color_dict[p.color] = color_dict.get(p.color) + 1

        color = max(color_dict, key=color_dict.get)
        self.point_list.append(Point(point.x, point.y, color))
        return color

    def classificator(self, k):
        self.point_list.clear()
        self.point_list.extend(self.init_points)
        success_rate = 0
        colors = ['red', 'green', 'blue', 'purple']

        color_counter = {
            'red': 0,
            'green': 0,
            'blue': 0,
            'purple': 0
        }

        while(len(self.point_list) < self.points_to_generate + len(self.init_points)):
            last_color = None
            rand_color = random.choice(colors)
            while(last_color == rand_color):
                rand_color = random.choice(colors)

            if(self.normal_generate()):
                if(color_counter[rand_color] < len(self.generated_points_dict[rand_color])):
                    point = self.generated_points_dict[rand_color][color_counter[rand_color]]
            else:
                if (color_counter[rand_color] < len(self.generated_points_dict[rand_color+ '_all'])):
                    point = self.generated_points_dict[rand_color + '_all'][color_counter[rand_color]]

            if(point):
                last_color = self.classify(point, k)
                color_counter[rand_color] = color_counter.get(rand_color) + 1

                if(last_color == rand_color):
                    success_rate += 1

        self.plot_points_list.append([self.point_list.copy(), k])
        print(f"[k = {k}] Successfully classified {success_rate} points out of {self.points_to_generate} ({(success_rate * 100) / self.points_to_generate} %)")

    def display(self):
        figure, axis = plt.subplots(2, 2)
        for i in range(0, len(self.plot_points_list)):
            pos1 = bin(i)[2:].zfill(2)[0]
            pos2 = bin(i)[2:].zfill(2)[1]
            axis[int(pos1), int(pos2)].set_title(label=f"k = {self.plot_points_list[i][1]}", fontsize=20)
            axis[int(pos1), int(pos2)].scatter(x=[point.x for point in self.plot_points_list[i][0]], y=[point.y for point in self.plot_points_list[i][0]], s=100, color=[point.color for point in self.plot_points_list[i][0]])
        plt.tight_layout()
        plt.savefig('classification')
        print('Result image was saved as \"classification.png\"')
        plt.show()

    def __init__(self, points, size, start_x, start_y):
        self.points_to_generate = points
        self.size = size
        self.start_x = start_x
        self.start_y = start_y
        self.init()
        self.generate_points()

def main():
    start = datetime.datetime.now()
    classification = Classification(20000, 10000, -5000, -5000)
    classification.classificator(1)
    classification.classificator(3)
    classification.classificator(7)
    classification.classificator(15)
    classification.display()
    end = datetime.datetime.now()
    print(f"Total time: {end-start}")

if __name__ == '__main__':
    main()

