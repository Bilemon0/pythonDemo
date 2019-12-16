import pylab


def findPayment(load, r, m):
    """假设load和r是浮点数，m是整数，
    返回一个总额为load，月利率r，期限m月的
    抵押贷款的每月还款额"""
    return load * ((r * (1 + r) ** m) / ((1 + r) ** m - 1))


class Mortgage(object):
    """用来建立不用种类抵押贷款的抽象类"""

    def __init__(self, loan, annRate, months):
        """loan，annRate为浮点数，month为整数
        创建一个总额为loan，期限为months月，年利率为annRate的新抵押贷款"""
        self.loan = loan  # 初始贷款额
        self.rate = annRate / 12  # 每月利率
        self.months = months  # 贷款期限/月
        self.paid = [0.0]  # 已支付的每月还款额列表
        self.outstanding = [loan]  # 每月的未支付贷款余额列表
        self.payment = findPayment(loan, self.rate, months)  # 每月需支付的金额
        self.legend = None

    def makePayment(self):
        """支付每月还款额"""
        self.paid.append(self.payment)
        reduction = self.payment - self.outstanding[-1] * self.rate
        self.outstanding.append(self.outstanding[-1] - reduction)

    def getTotalPaid(self):
        """返回至今为止的支付总额"""
        return sum(self.paid)

    def __str__(self):
        return self.legend

    def plotPayments(self, style):
        pylab.plot(self.paid[1:], style, label=self.legend)

    def plotBalance(self, style):
        pylab.plot(self.outstanding, style, label=self.legend)

    def plotTotPd(self, style):
        totPd = [self.paid[0]]
        for i in range(1, len(self.paid)):
            totPd.append(totPd[-1] + self.paid[i])
        pylab.plot(totPd, style, label=self.legend)

    def plotNet(self, style):
        totPd = [self.paid[0]]
        for i in range(1, len(self.paid)):
            totPd.append(totPd[-1] + self.paid[i])
        equityAcquired = pylab.array([self.loan] * len(self.outstanding))
        equityAcquired = equityAcquired - pylab.array(self.outstanding)
        net = pylab.array(totPd)-equityAcquired
        pylab.plot(net, style, label=self.legend)


class Fixed(Mortgage):
    def __init__(self, loan, r, months):
        Mortgage.__init__(self, loan, r, months)
        self.legend = 'Fixed, ' + str(round(r * 100, 2)) + '%'


class FixedWithPts(Mortgage):
    def __init__(self, loan, r, months, pts):
        Mortgage.__init__(self, loan, r, months)
        self.pts = pts
        self.paid = [loan * (pts / 100)]
        self.legend = 'Fixed, ' + str(round(r * 100, 2)) + '%，' \
                      + str(pts) + ' points'


class TwoRate(Mortgage):
    def __init__(self, loan, r, months, teaserRate, teaserMonths):
        Mortgage.__init__(self, loan, r, months)
        self.teaserMonths = teaserMonths
        self.teaserRate = teaserRate
        self.nextRate = r / 12
        self.legend = str(teaserRate * 100) + '% for ' \
                      + str(self.teaserMonths) + ' months, then ' \
                      + str(round(r * 100, 2)) + '%'

    def makePayment(self):
        if len(self.paid) == self.teaserMonths + 1:
            self.rate = self.nextRate
            self.payment = findPayment(self.outstanding[-1], self.rate,
                                       self.months - self.teaserMonths)
        Mortgage.makePayment(self)


def plotMortgages(morts, amt):
    def labelPlot(figure, title, xLabel, yLabel):
        pylab.figure(figure)
        pylab.title(title)
        pylab.xlabel(xLabel)
        pylab.ylabel(yLabel)
        pylab.legend(loc='best')
    # 给图编号赋名
    styles = ['k-', 'k-.', 'k:']
    payments, cost, balance, netCost = 0, 1, 2, 3
    for i in range(len(morts)):
        pylab.figure(payments)
        morts[i].plotPayments(styles[i])
        pylab.figure(cost)
        morts[i].plotTotPd(styles[i])
        pylab.figure(balance)
        morts[i].plotBalance(styles[i])
        pylab.figure(netCost)
        morts[i].plotNet(styles[i])
    labelPlot(payments, 'Monthly Payments of $' + str(amt) + ' Mortgages', 'Months', 'Monthly Payments')
    labelPlot(cost, 'Cash Outlay of $' + str(amt) + 'Mortgages', 'Months', 'Total Payments')
    labelPlot(balance, 'Balance Remaining of $' + str(amt) + 'Mortgages', 'Months', 'Remaining Loan Balance of $')
    labelPlot(netCost, 'Net Cost of $' + str(amt) + ' Mortgages', 'Months', 'Payments - Equity $')


def compareMortgage(amt, years, fixedRate, pts, ptsRate, varRate1, varRate2, varMonths):
    totMonths = years * 12
    fixed1 = Fixed(amt, fixedRate, totMonths)
    fixed2 = FixedWithPts(amt, ptsRate, totMonths, pts)
    twoRate = TwoRate(amt, varRate2, totMonths, varRate1, varMonths)
    morts = [fixed1, fixed2, twoRate]
    for m in range(totMonths):
        for mort in morts:
            mort.makePayment()
    plotMortgages(morts, amt)
    # for m in morts:
    #     print(m)
    #     print(m.paid)
    #     print(m.outstanding)
    #     print(' Total payment = $' + str(int(m.getTotalPaid())))


compareMortgage(amt=200000, years=30, fixedRate=0.07, pts=3.25, ptsRate=0.05, varRate1=0.045,
                varRate2=0.095, varMonths=48)
