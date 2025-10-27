data = read.table("data.txt")
k = nrow(data)
print(k)

n = nrow(mtcars) - (k%%5)
print(n)

mt = head(mtcars, n)

wt_am0 = mt$wt[mt$am == 0]
n = length(wt_am0)
s = sd(wt_am0)
SE = s / sqrt(n)
E = qt(0.995, df = n - 1) * SE
xbar = mean(wt_am0)
CI = xbar + c(-E, E)
print(CI)

wt_am1 = mt$wt[mt$am == 1]
n = length(wt_am1)
s = sd(wt_am1)
SE = s / sqrt(n)
xbar = mean(wt_am1)
t_stat = (xbar - 2.1) / SE
p_value = pt(t_stat, df = n - 1, lower.tail = FALSE)
print(p_value)

diff = data[[2]] - data[[3]]
n = length(diff)
mean_diff = mean(diff)
sd_diff = sd(diff)
SE_diff = sd_diff / sqrt(n)
E_diff = qt(0.975, df = n - 1) * SE_diff
CI_diff = mean_diff + c(-E_diff, E_diff)
print(CI_diff)

x1 = data[[2]]
x2 = data[[3]]
n1 = length(x1)
n2 = length(x2)
mean1 = mean(x1)
mean2 = mean(x2)
sd1 = sd(x1)
sd2 = sd(x2)
SE_ind = sqrt((sd1^2 / n1) + (sd2^2 / n2))
df = ( (sd1^2 / n1) + (sd2^2 / n2) )^2 / 
     ( ( (sd1^2 / n1)^2 / (n1 - 1) ) + ( (sd2^2 / n2)^2 / (n2 - 1) ) )
E_ind = qt(0.975, df = df) * SE_ind
mean_diff_ind = mean1 - mean2
CI_ind = mean_diff_ind + c(-E_ind, E_ind)
print(CI_ind)