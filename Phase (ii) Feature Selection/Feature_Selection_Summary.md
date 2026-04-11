# Feature Selection Summary

## Combined

| CORR (|r| < 0.5) | ANOVA (Top 30%) | FLAML (> 0.03) | PSO | WOA |
|---|---|---|---|---|
| IO_Operations | Root_DIR_Access | IO_Operations | IO_Operations | IO_Operations |
| File_Operations | Home_DIR_Access | File_Operations | File_Operations | File_Operations |
| Network_Operations | User_DIR_Access | Time_Operations | Network_Operations | Network_Operations |
| Time_Operations | Other_DIR_Access | Process_Operations | Process_Operations | Process_Operations |
| Security_Operations | IO_Operations | Write_Processes | Read_Processes | Read_Data_Transfer |
| Process_Operations | File_Operations | Read_Data_Transfer | Write_Processes | Write_Data_Transfer |
| Read_Processes | Network_Operations | Local_Port_Access | Read_Data_Transfer | File_Access_Processes |
| Write_Processes | Read_Processes | Remote_Port_Access | Write_Data_Transfer | Total_Dependencies_List |
| Read_Data_Transfer | Write_Processes | Total_Dependencies | File_Access_Processes | Indirect_Dependencies_List |
| Write_Data_Transfer | Write_Data_Transfer | Direct_Dependencies | Total_Dependencies | Home_DIR_Access |
| File_Access_Processes | File_Access_Processes | Indirect_Dependencies | Root_DIR_Access | Local_IPs_Access |
| Total_Dependencies | Direct_Dependencies | Pattern_1 | Temp_DIR_Access | Remote_IPs_Access |
| Direct_Dependencies |  | Pattern_2 | Home_DIR_Access | Local_Port_Access |
| Indirect_Dependencies |  | Pattern_3 | Local_Port_Access | Remote_Port_Access |
| Root_DIR_Access |  | Pattern_4 | Total_Dependencies | Total_Dependencies |
| Temp_DIR_Access |  | Pattern_5 | Pattern_2 | Indirect_Dependencies |
| Sys_DIR_Access |  | Pattern_6 | Pattern_7 | Pattern_1 |
| State_Transition |  |  | Pattern_8 | Pattern_2 |
| Local_IPs_Access |  |  | Pattern_9 | Pattern_5 |
| Total_Dependencies |  |  |  | Pattern_6 |
| Pattern_1 |  |  |  | Pattern_7 |
| Pattern_2 |  |  |  | Pattern_8 |
| Pattern_3 |  |  |  | Pattern_9 |
| Pattern_4 |  |  |  | Write_Processes |
| Pattern_5 |  |  |  |  |
| Pattern_6 |  |  |  |  |
| Pattern_7 |  |  |  |  |
| Pattern_8 |  |  |  |  |
| Pattern_9 |  |  |  |  |
| Pattern_10 |  |  |  |  |
| Total = 30 | Total = 12 | Total = 17 | Total = 19 | Total = 24 |

## Filetop

| CORR (|r| < 0.5) | ANOVA (Top 30%) | FLAML (> 0.03) | PSO | WOA |
|---|---|---|---|---|
| Total_Reads | Total_Write_Data_Transfer | Total_Reads | Total_Reads | Total_Reads |
| Total_Writes | Read_Processes | Total_Writes | Total_Writes | Read_Processes |
| Read_Processes | Write_Processes | Total_Read_Data_Transfer | Total_Write_Data_Transfer | Total_Write_Data_Transfer |
| Write_Processes | Write_Data_Transfer_Processes | Total_Write_Data_Transfer | Read_Processes | File_Access_Processes |
| Read_Data_Transfer_Processes | File_Access_Processes | Read_Processes | Read_Data_Transfer_Processes | Read_Data_Transfer_Processes |
| Write_Data_Transfer_Processes |  | Write_Processes | Write_Data_Transfer_Processes | Write_Data_Transfer_Processes |
| File_Access_Processes |  | Read_Data_Transfer_Processes | File_Access_Processes |  |
|  |  | Write_Data_Transfer_Processes |  |  |
|  |  | File_Access_Processes |  |  |
| Total = 7 | Total = 5 | Total = 9 | Total = 7 | Total = 6 |

## Opensnoop

| CORR (|r| < 0.5) | ANOVA (Top 30%) | FLAML (> 0.03) | PSO | WOA |
|---|---|---|---|---|
| Total_Paths | Python_Related_Keywords | Total_Paths | Total_Paths | Total_Paths |
| File_Descriptor | Install_Package_Keywords | Total_Error | Total_File_Descriptor | Total_File_Descriptor |
| Temporary_DIR_Installation | Home_DIR_Installation | Total_File_Descriptor | Python_Related_Keywords | Python_Related_Keywords |
| Sys_Access | User_Access | Python_Related_Keywords | Install_Package_Keywords | Root_DIR_Installation |
|  |  | Install_Package_Keywords | Root_DIR_Installation | Temporary_DIR_Installation |
|  |  | Root_DIR_Installation | Temporary_DIR_Installation | User_Access |
|  |  | Temporary_DIR_Installation | Home_DIR_Installation | Sys_Access |
|  |  | Home_DIR_Installation | User_Access | Other_DIR_Installation |
|  |  | User_Access | Sys_Access |  |
|  |  | Sys_Access |  |  |
|  |  | Etc_DIR_Installation |  |  |
| Total = 4 | Total = 4 | Total = 11 | Total = 9 | Total = 8 |

## Install

| CORR (|r| < 0.5) | ANOVA (Top 30%) | FLAML (> 0.03) | PSO | WOA |
|---|---|---|---|---|
| Total_Dependency_Count | Direct_Dependency_Count | Direct_Dependencies | Total_Dependencies | Direct_Dependency_Count |
| Total_Dependencies | Direct_Dependencies | Indirect_Dependencies | Direct_Dependency_Count | Direct_Dependencies |
| Direct_Dependencies |  |  | Indirect_Dependencies | Indirect_Dependency_Count |
| Indirect_Dependencies |  |  |  | Indirect_Dependencies |
| Total = 4 | Total = 2 | Total = 2 | Total = 3 | Total = 4 |

## TCP

| CORR (|r| < 0.5) | ANOVA (Top 30%) | FLAML (> 0.03) | PSO | WOA |
|---|---|---|---|---|
| Total_Entries | Total_Entries | Python_Related_Process | Total_Entries | Local_Port_Access |
| State_Transition | Remote_IP_Address_Access | State_Transition | Python_Related_Process | Unique_C-COMM |
|  | Remote_Port_Access | Local_IP_Address_Access | Local_IP_Address_Access | Python_Related_Process |
|  |  | Local_Port_Access | Local_Port_Access | Remote_Port_Access |
|  |  | Remote_Port_Access | Remote_Port_Access | Remote_IP_Address_Access |
| Total = 2 | Total = 3 | Total = 5 | Total = 5 | Total = 5 |

## SysCall

| CORR (|r| < 0.5) | ANOVA (Top 30%) | FLAML (> 0.03) | PSO | WOA |
|---|---|---|---|---|
| Unique_IO_Operations_List | Unique_Process_Management_Operations_List | Unique_IO_Operations_List | Unique_Process_Management_Operations | Unique_Process_Management_Operations |
| Unique_IPC_Operations_List | Unique_IO_Operations_List | Unique_Time_Operations_List | Unique_Process_Management_Operations_List | Unique_IO_Operations_List |
| Unique_Security_Operations_List | Unique_Time_Operations_List | Unique_IPC_Operations_List | Unique_IO_Operations_List | Unique_Time_Operations_List |
| Unique_Miscellaneous_Operations_List | Unique_IPC_Operations_List | Unique_Security_Operations_List | Unique_Time_Operations_List | Unique_IPC_Operations_List |
|  | Unique_Security_Operations_List | Unique_Miscellaneous_Operations_List | Unique_IPC_Operations_List | Unique_Security_Operations_List |
|  | Unique_Miscellaneous_Operations_List |  | Unique_Security_Operations_List | Unique_Miscellaneous_Operations_List |
|  |  |  | Unique_Miscellaneous_Operations_List |  |
| Total = 4 | Total = 6 | Total = 5 | Total = 7 | Total = 6 |

## Pattern

| CORR (|r| < 0.5) | ANOVA (Top 30%) | FLAML (> 0.03) | PSO | WOA |
|---|---|---|---|---|
| Pattern_1 | Pattern_1 | Pattern_2 | Pattern_1 | Pattern_3 |
| Pattern_2 | Pattern_3 | Pattern_3 | Pattern_4 | Pattern_4 |
| Pattern_3 | Pattern_6 | Pattern_4 | Pattern_10 | Pattern_5 |
| Pattern_4 | Pattern_7 | Pattern_5 | Pattern_5 | Pattern_8 |
| Pattern_5 |  | Pattern_7 | Pattern_9 | Pattern_2 |
| Pattern_6 |  | Pattern_8 |  | Pattern_10 |
| Pattern_7 |  | Pattern_9 |  |  |
| Pattern_8 |  | Pattern_10 |  |  |
| Pattern_9 |  |  |  |  |
| Pattern_10 |  |  |  |  |
| Total = 10 | Total = 4 | Total = 8 | Total = 5 | Total = 6 |

Source: user-provided tables.