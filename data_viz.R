library(ggplot2)

# Read DH data
DH_values <- read.table(file = "/Volumes/lsi-davidhs/MD/anti_DA/simulations/ZWP_CitL_WT/ZWP_DH.dat", header = TRUE)





# Create conformer plot
count_table <- table(DH_values$DH1 > 0)
anti_label <- paste("Anti (n = ", as.character(count_table[1]), ")", sep = "")
syn_label <-  paste("Syn (n = ", as.character(count_table[2]), ")", sep = "")
conformer_plot <- ggplot(DH_values, aes(x = DH2, y = DH1, fill = DH1 > 0)) +
  geom_point(size = 1, shape = 21) +
  scale_color_manual(values = c("black"), guide = "none") +
  scale_fill_manual(values = c("blue", "red"), labels = c(anti_label, syn_label)) +
  labs(x = expression(paste("Diene ", Theta, " (º)")), y = expression(paste("Dieneophile ", Theta, " (º)")), fill = "Conformation", size = 20) +
  scale_x_continuous(limits = c(-180, 180)) +
  scale_y_continuous(limits = c(-180, 180)) +
  theme(axis.text = element_text(size = 20),
        legend.title = element_text(size = 16),
        legend.text = (element_text(size = 16)),
        axis.title = element_text(size = 20),
        legend.position = "inside",
        legend.position.inside = c(0.25, 0.75))
# Display conformer plot
print(conformer_plot)
# Save conformer plot in a specific directory
ggsave("/Volumes/lsi-davidhs/MD/anti_DA/simulations/ZWP_CitL_WT/DH_plot.tiff", conformer_plot, width = 5.6, height = 4, dpi = 300)



# Read ZWP-NAP data
ZWP_NAP_dist <- read.table(file = "/Volumes/lsi-davidhs/MD/anti_DA/simulations/ZWP_CitL_WT/NAP_dist.dat", header = TRUE)


# Create NAP distance plot
ZWP_NAP_dist$time <- ZWP_NAP_dist$Frame * 0.05
NAP_dist <- ggplot(ZWP_NAP_dist, aes(x = time, y = ZWP_NAP1)) +
  geom_line() +
  labs(x = "Time (ns)", y = "ZWP <-> NAP distance (\u00C5)") +
  theme(axis.text = element_text(size = 16),
        legend.title = element_text(size = 16),
        legend.text = (element_text(size = 16)),
        axis.title = element_text(size = 16)) +
  scale_y_continuous(limits = c(2, 8))

# Save NAP distance plot in a specific directory
ggsave("/Volumes/umms-maom/projects/IMDAase/md/simulations/Ctdp_mono_diene/PMC_lig/rep1/plots_data/NAP_dist.pdf", NAP_dist, width = 7, height = 6, dpi = 300)

# Display NAP distance plot
print(NAP_dist)

# Display mean ZWP-NAP1 distance
mean(ZWP_NAP_dist$ZWP_NAP1)

