"""
SUPER TEMPORARY
"""
#TODO CHANGE THIS

import matplotlib.pylab as plt
import matplotlib as m

import pandas as pd
import numpy as np


class ComparisonPlot:

    @staticmethod
    def formatting():
        plt.rcParams["figure.figsize"] = (14, 5)
        plt.rcParams["figure.dpi"] = 600
        plt.rcParams['axes.linewidth'] = 2
        plt.rcParams["font.size"] = 14
        plt.rcParams["legend.fontsize"] = "x-large"
        plt.rcParams['xtick.labelsize'] = 'x-large'
        plt.rcParams['ytick.labelsize'] = 'x-large'
        plt.rcParams.update({'figure.autolayout': True})

    @staticmethod
    def setup(df):
        p = 0.75
        of_interest = df.predict_fpa > p

        df["first_person_alcohol"] = 0
        df["first_person_alcohol"][of_interest] = 1
        fp_cols = ['predict_present', 'predict_future', 'predict_past']
        new_fp_cols = ["casual", "looking", "reflecting"]
        for new_name, old_name in zip(new_fp_cols, fp_cols):
            df[new_name] = df[old_name] > 0.6

    @staticmethod
    def centered_95int(data):
        return 1.96 * (data.std() / np.sqrt(len(data)))

    @staticmethod
    def compare_fpl_weeks(dfs, plot_output_dir):
        """
        dfs: list of dataframes with DateTime index
        """
        temp = pd.DataFrame()
        for df in dfs:
            _temp = df.groupby([df.index.dayofweek, df.index.hour]).agg(
                {"mean": "mean", "err": centered_95int}
            )
            temp = pd.concat([temp, _temp], axis=1)

        stds = temp.ix[:, 1::2].rolling(window=3).mean()
        means = temp.ix[:, 0::2].rolling(window=3).mean()

        num_weeks = len(means.columns)

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        for i in range(num_weeks):
            ax.plot(range(len(means)), means.ix[:, i], '.-', label="week" + str(i + 1))

        ax.set_xlim([0, 24 * 7])
        ax.set_xticks(range(0, 24 * 7, 24))
        ax.set_xticklabels(["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"], rotation=12)
        ax.set_title("comparison over week")
        ax.set_ylabel("Proportion of all tweets")
        ax.legend(loc="best")
        ax.grid()
        #     plt.savefig(plot_output_dir + "reflecting_comparison.png")

    @staticmethod
    def plot_fps_week(df, folder):
        temp = df.groupby([df.index.dayofweek, df.index.hour]).agg(
            {
                _: {"mean": "mean", "err": ComparisonPlot.centered_95int} for _ in ['casual', 'looking', 'reflecting']
                }
        )
        means = pd.rolling_mean(temp[[1, 3, 5]], 3)

        stds = pd.rolling_mean(temp[[0, 2, 4]], 3)

        means.columns = [col[0] for col in means.columns.values]
        stds.columns = [col[0] for col in stds.columns.values]

        fig = plt.figure()

        ax = fig.add_subplot(111)
        ax.plot(range(len(means)), means.casual, "r.-", label="casual")
        ax.fill_between(
            x=range(len(means)),
            y1=means.casual - stds.casual,
            y2=means.casual + stds.casual,
            color='r', alpha=.1
        )

        ax.plot(range(len(means)), means.looking, "g.:", label="looking")
        ax.fill_between(
            x=range(len(means)),
            y1=means.looking - stds.looking,
            y2=means.looking + stds.looking,
            color="g", alpha=.1
        )

        ax.plot(range(len(means)), means.reflecting, "b.--", label="reflecting")
        ax.fill_between(
            x=range(len(means)),
            y1=means.reflecting - stds.reflecting,
            y2=means.reflecting + stds.reflecting,
            color="b", alpha=.1
        )

        ax.set_xlim([0, 24 * 7])

        ax.set_xticks(range(0, 24 * 7, 24))
        ax.set_xticklabels(["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"], rotation=12)
        ax.set_title("Alcohol - First Person state over week")
        ax.set_ylabel("Proportion of all tweets")
        ax.legend(loc="best")
        ax.grid()
        #     plt.savefig(folder + "plt_levels_weekhour_test_alc.png")