from Base import Base

import warnings
warnings.filterwarnings('ignore')

import os
import plotly.express as px
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

import pandas as pd
from sklearn.decomposition import PCA

import plotly.graph_objs as go
import plotly.tools as tls
# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.image as mpimg
# import matplotlib
# from sklearn.manifold import TSNE
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

class Validation(Base):
    def generateHeadMap(self):
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
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                    square=True, linewidths=.5, cbar_kws={"shrink": .5})

        plt.title('Correlation Heatmap (for the MEAN variables)', fontsize = 20)
        plt.xticks(fontsize = 10)
        plt.yticks(fontsize = 10)

        plt.savefig(os.path.join(self.data_dir, "Corr_Heatmap.png"))
    
    def generatePCAChart(self):
        features = [col for col in self.df.columns if col not in ['filename', 'label']]
        pca = PCA()
        components = pca.fit_transform(self.df[features])
        labels = {
            str(i): f"{var:.1f}%"
            for i, var in enumerate(pca.explained_variance_ratio_ * 100)
        }
        fig =  px.scatter_matrix(
            components,
            labels=labels,
            dimensions=range(2),
            color=self.df["label"],
            hover_name=self.df['filename'],
            height=1000
        )
        fig.update_traces(diagonal_visible=False)
        fig.show()
        fig.write_image(os.path.join(self.data_dir, "Scattert.png"))
        
    def generateInformation(self):
        print("Dataset has",self.df.shape)
        print("Count of Positive and Negative samples")
        print("Columns with NA values are",list(self.df.columns[self.df.isnull().any()]))
        print(self.df.label.value_counts().reset_index())
        

    def generateBetterPCACharts(self):
        # save the labels to a Pandas series target
        target = self.df['label']
        # Drop the label feature
        self.df = self.df.drop(["label", "filename", "length"], axis=1)
        
        # Standardize the data
        X = self.df.values
        X_std = StandardScaler().fit_transform(X)

        # Calculating Eigenvectors and eigenvalues of Cov matirx
        mean_vec = np.mean(X_std, axis=0)
        cov_mat = np.cov(X_std.T)
        eig_vals, eig_vecs = np.linalg.eig(cov_mat)
        # Create a list of (eigenvalue, eigenvector) tuples
        eig_pairs = [ (np.abs(eig_vals[i]),eig_vecs[:,i]) for i in range(len(eig_vals))]

        # Sort the eigenvalue, eigenvector pair from high to low
        eig_pairs.sort(key = lambda x: x[0], reverse= True)

        # Calculation of Explained Variance from the eigenvalues
        tot = sum(eig_vals)
        var_exp = [(i/tot)*100 for i in sorted(eig_vals, reverse=True)] # Individual explained variance
        cum_var_exp = np.cumsum(var_exp) # Cumulative explained variance
        
        trace1 = go.Scatter(
            x=list(range(784)),
            y= cum_var_exp,
            mode='lines+markers',
            name="'Cumulative Explained Variance'",
            hoverinfo= cum_var_exp,
            line=dict(
                shape='spline',
                color = 'goldenrod'
            )
        )
        trace2 = go.Scatter(
            x=list(range(784)),
            y= var_exp,
            mode='lines+markers',
            name="'Individual Explained Variance'",
            hoverinfo= var_exp,
            line=dict(
                shape='linear',
                color = 'black'
            )
        )
        fig = tls.make_subplots(insets=[{'cell': (1,1), 'l': 0.7, 'b': 0.3}],
                                print_grid=True)

        fig.append_trace(trace1, 1, 1)
        fig.append_trace(trace2,1,1)
        fig.layout.xaxis = dict(range=[0, 80])
        fig.layout.yaxis = dict(range=[0, 60])
        fig['data'] += [go.Scatter(x= list(range(784)) , y=cum_var_exp, xaxis='x2', yaxis='y2', name = 'Cumulative Explained Variance')]
        fig['data'] += [go.Scatter(x=list(range(784)), y=var_exp, xaxis='x2', yaxis='y2',name = 'Individual Explained Variance')]

        # fig['data'] = data
        # fig['layout'] = layout
        # fig['data'] += data2
        # fig['layout'] += layout2
        # py.iplot(fig, filename='inset example')
        
                
    def generateOldPCACharts(self):
        data = self.df.iloc[0:, 1:]
        y = data['label']
        X = data.loc[:, data.columns != 'label']

        # normalize
        cols = X.columns
        min_max_scaler = MinMaxScaler()
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
        plt.yticks(fontsize = 10);
        plt.xlabel("Principal Component 1", fontsize = 15)
        plt.ylabel("Principal Component 2", fontsize = 15)
        plt.savefig("PCA_Scattert.png")