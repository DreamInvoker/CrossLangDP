def show(c, total, interval="", DoneInfo='Done!'):
    """
        输出进度和百分比
    :param c: 当前完成任务数
    :param total: 总任务数
    :param interval: 已消耗的时间
    :param DoneInfo: 完成后的提示
    :return:
    """
    per = int(c / total * 100)
    k = per + 1
    s = '>' * (per // 2) + '-' * ((100 - k) // 2)
    print('\r{}[{}%---{}/{}]\ttime:{}.'.format(s, per, c, total, interval), end='')
    if per == 100:
        print('\n{}'.format(DoneInfo))

