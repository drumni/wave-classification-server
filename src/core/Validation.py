from src.core.Base import Base

# Let us load in the relevant Python modules

import os
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import missingno as msno
import plotly.tools as tls
import plotly.offline as py
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import sklearn.preprocessing as skp
from sklearn.decomposition import PCA

# import plotly.tools as tls
# import plotly.express as px
# import plotly.graph_objs as go
# from collections import Counter
# from sklearn.decomposition import PCA
# from sklearn.preprocessing import StandardScaler
# from sklearn.feature_selection import mutual_info_classif

sns.set_style('whitegrid')
py.init_notebook_mode(connected=True)
warnings.filterwarnings('ignore')

class Validation(Base):
    def generateExplainedVariance(self):
        pass
    
    def generateBPMPlot(self):
        x = self.df[["label", "tempo"]]

        fig, ax = plt.subplots(figsize=(16, 8))
        sns.boxplot(x = "label", y = "tempo", data = x, palette = 'husl')

        plt.title('BPM Boxplot for Genres', fontsize = 20)
        plt.xticks(fontsize = 14)
        plt.yticks(fontsize = 10)
        plt.xlabel("Genre", fontsize = 15)
        plt.ylabel("BPM", fontsize = 15)
        plt.savefig(os.path.join(self.data_dir, "BPM_BoxPlot.png"))
    
    def generateMissingValues(self):
        data = self.df
        fig = msno.matrix(df=data, figsize=(20, 14), color=(0.42, 0.1, 0.05))
        _fig = fig.get_figure()
        _fig.savefig(os.path.join(self.data_dir, 'Missing_MatrixPlot.png'))
    
    def generateImportancePlot(self):
        data = self.df
        from sklearn.ensemble import GradientBoostingClassifier
        gb = GradientBoostingClassifier(n_estimators=100, max_depth=3, min_samples_leaf=4, max_features=0.2, random_state=0)
        gb.fit(data.drop(["label", "filename", 'index'],axis=1), data.label)
        features = data.drop(["label", "filename", 'index'],axis=1).columns.values
        print("----- Training Done -----")
        
        # Scatter plot 
        trace = go.Scatter(
            y = gb.feature_importances_,
            x = features,
            mode='markers',
            marker=dict(
                sizemode = 'diameter',
                sizeref = 1,
                size = 13,
                #size= rf.feature_importances_,
                #color = np.random.randn(500), #set color equal to a variable
                color = gb.feature_importances_,
                colorscale='Portland',
                showscale=True
            ),
            text = features
        )
        data = [trace]

        layout= go.Layout(
            autosize= True,
            title= 'Gradient Boosting Machine Feature Importance',
            hovermode= 'closest',
            xaxis= dict(
                ticklen= 5,
                showgrid=False,
                zeroline=False,
                showline=False
            ),
            yaxis=dict(
                title= 'Feature Importance',
                showgrid=False,
                zeroline=False,
                ticklen= 5,
                gridwidth= 2
            ),
            showlegend= False
        )
        fig = go.Figure(data=data, layout=layout)
        py.iplot(fig)
        fig.write_image(os.path.join(self.data_dir, "FeatureImportance_DotsPlot.png"))
        
        x, y = (list(x) for x in zip(*sorted(zip(gb.feature_importances_, features), 
                                                                    reverse = False)))
        trace2 = go.Bar(
            x=x ,
            y=y,
            marker=dict(
                color=x,
                colorscale = 'Viridis',
                reversescale = True
            ),
            name='Gradient Boosting Classifer Feature importance',
            orientation='h',
        )

        layout = dict(
            title='Barplot of Feature importances',
            width = 900, height = 2000,
            yaxis=dict(
                showgrid=False,
                showline=False,
                showticklabels=True,
            ))

        fig1 = go.Figure(data=[trace2])
        fig1['layout'].update(layout)
        py.iplot(fig1)
        fig1.write_image(os.path.join(self.data_dir, "FeatureImportance_BarPlot.png"))
    
    def generateHeadMapMean(self):
        # Computing the Correlation Matrix
        spike_cols = [col for col in self.df.columns if 'mean' in col]
        corr = self.df[spike_cols].corr()

        # Generate a mask for the upper triangle
        mask = np.triu(np.ones_like(corr, dtype=np.bool))

        # Set up the matplotlib figure
        f, ax = plt.subplots(figsize=(16, 11))

        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(0, 25, as_cmap=True, s = 90, l = 45, n = 5)

        # Draw the heatmap with the mask and correct aspect ratio
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                    square=True, linewidths=.5, cbar_kws={"shrink": .5})

        plt.title('Correlation Heatmap (for the MEAN variables)', fontsize = 20)
        plt.xticks(fontsize = 10)
        plt.yticks(fontsize = 10)

        plt.savefig(os.path.join(self.data_dir, "CorrelationHeatmapPlotMean.png"))
        
    def generateHeadMapVar(self):
        # Computing the Correlation Matrix
        spike_cols = [col for col in self.df.columns if 'var' in col]
        corr = self.df[spike_cols].corr()

        # Generate a mask for the upper triangle
        mask = np.triu(np.ones_like(corr, dtype=np.bool))

        # Set up the matplotlib figure
        f, ax = plt.subplots(figsize=(16, 11))

        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(0, 25, as_cmap=True, s = 90, l = 45, n = 5)

        # Draw the heatmap with the mask and correct aspect ratio
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                    square=True, linewidths=.5, cbar_kws={"shrink": .5})

        plt.title('Correlation Heatmap (for the VAR variables)', fontsize = 20)
        plt.xticks(fontsize = 10)
        plt.yticks(fontsize = 10)

        plt.savefig(os.path.join(self.data_dir, "CorrelationHeatmapPlotVar.png"))

        
    def generateOldPCACharts(self):
        data = self.df
        y = data['label']
        X = data
        X.drop(['label', 'filename'], axis=1, inplace=True)
        
        # normalize
        cols = X.columns
        min_max_scaler = skp.MinMaxScaler()
        np_scaled = min_max_scaler.fit_transform(X)
        X = pd.DataFrame(np_scaled, columns = cols)

        # Top 2 pca components
        from sklearn.decomposition import PCA

        pca = PCA(n_components=2)
        principalComponents = pca.fit_transform(X)
        principalDf = pd.DataFrame(data = principalComponents, columns = ['pc1', 'pc2'])

        # concatenate with target label
        finalDf = pd.concat([principalDf, y], axis = 1)

        plt.figure(figsize = (16, 9))
        sns.scatterplot(x = "pc1", y = "pc2", data = finalDf, hue = "label", alpha = 0.7, s = 100);

        plt.title('PCA on Genres', fontsize = 20)
        plt.xticks(fontsize = 14)
        plt.yticks(fontsize = 10)
        plt.xlabel("Principal Component 1", fontsize = 15)
        plt.ylabel("Principal Component 2", fontsize = 15)
        plt.savefig(os.path.join(self.data_dir, "PCA_ScattertPlot.png"))