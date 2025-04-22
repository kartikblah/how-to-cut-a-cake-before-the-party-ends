

class PiecewiseLinearValuation:
    def __init__(self, segments):
        self.segments = sorted(segments, key=lambda x: x[0])
        self.eps = 1e-6 


    # eval is correct, i have checked. 
    def eval(self, a, b):
        total = 0.0
        for (start, end, slope, intercept) in self.segments:
            s = max(start, a)
            e = min(end, b)
            if s >= e:
                continue
            # Integrate linear function
            if slope == 0:
                total += intercept * (e - s)
            else:
                total += (0.5 * slope * (e**2 - s**2)) + (intercept * (e - s))
        return total

    def cut(self, a, w):
        # print(self.segments)
        if w <= 0:
            return a
        remaining = w
        current = a
        for (start, end, slope, intercept) in self.segments:
            if current >= end:
                continue
            s = max(start, current)
            if s >= end:
                continue
            if slope == 0:
                if intercept == 0:
                    continue
                y_candidate = s + remaining / intercept
                # print("y_candidate", y_candidate)
                # print("end", end)
                if y_candidate <= end:
                    return min(y_candidate, 1.0)
                else:
                    consumed = intercept * (end - s)
                    remaining -= consumed
                    current = end
            else:
                temp = self.eval(s, end)
                if temp < remaining:
                    consumed = temp
                    remaining -= consumed
                    current = end
                    continue
                else : 
                    # Solve quadratic equation for y
                    C = (0.5 * slope * (s**2)) + (intercept * s) + remaining
                    # 0.5 * slope * y^2 + intercept * y - C = 0
                    # Discriminant: b^2 - 4ac
                    a_coeff = 0.5 * slope 
                    b = intercept
                    c = -C
                    # C is the area consumed so far
                    # We need to find y such that the area from s to y equals remaining
                    # C = area from s to y
                    disc = (b**2) - (4 * a_coeff * c)
                    if(disc<0):
                        # print temp and remaining
                        # print("temp", temp)
                        # print("remaining", remaining)
                        # print(disc)
                        raise ValueError("No real solution exists for the quadratic equation.")
                    sol1 = (-b + (disc**0.5)) / (2 * a_coeff)
                    sol2 = (-b - (disc**0.5)) / (2 * a_coeff)
                    final = sol1
                    # if slope > 0:
                    #     final = sol2
                    # else : 
                    #     final = sol1

                    if(sol2>= s and sol2<=end):
                        final = sol2
                    # if final >= current and final <= end:
                    return min(final, 1.0)
                
        
        # raise error
        # print("the cut required was ")
        # print(a, w)
        return None