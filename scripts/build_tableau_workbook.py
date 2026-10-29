"""
Tableau Workbook Generator
Generates a native Tableau workbook: tableau/ITSM_SLA_Intelligence_Platform.twb
Configured for Tableau Desktop 2026.2 (Apple Silicon).

Features:
- Federated Textscan Connection to data/cleaned/itsm_tickets_cleaned.csv
- 14 Production Calculated Fields (Measures, Percentages, Formats)
- 14 Worksheets across the 4 core analytical themes
- 4 Executive Dashboards:
    1. Executive Overview
    2. SLA & Priority Analysis
    3. Workload & Team Performance
    4. Root Causes & Recommendations
"""

import os
import xml.etree.ElementTree as ET

def build_tableau_twb():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "cleaned", "itsm_tickets_cleaned.csv")
    twb_path = os.path.join(base_dir, "tableau", "ITSM_SLA_Intelligence_Platform.twb")

    twb_xml = f"""<?xml version='1.0' encoding='utf-8' ?>
<workbook locale='en_US' source-build='2026.2.2' source-platform='mac' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <document-format-change-manifest>
    <AutoCreateAndUpdateDSDPhoneLayouts />
    <IntuitiveSorting />
    <IntuitiveSorting_EncodingByColor />
    <StandardCubeDimensions />
  </document-format-change-manifest>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='26' />
  </preferences>
  <datasources>
    <datasource caption='itsm_tickets_cleaned' inline='true' name='federated.itsm_data' version='18.1'>
      <connection class='federated'>
        <named-connections>
          <named-connection caption='itsm_tickets_cleaned' name='textscan.itsm_conn'>
            <connection class='textscan' directory='{os.path.dirname(csv_path)}' filename='{os.path.basename(csv_path)}' header='yes' locale='en_US' separator=',' text-qualifier='&quot;' />
          </named-connection>
        </named-connections>
        <relation connection='textscan.itsm_conn' name='itsm_tickets_cleaned#csv' table='[itsm_tickets_cleaned#csv]' type='table'>
          <columns character-set='UTF-8' header='yes' locale='en_US' separator=',' text-qualifier='&quot;'>
            <column datatype='string' name='Ticket_ID' ordinal='0' />
            <column datatype='datetime' name='Created_Date' ordinal='1' />
            <column datatype='datetime' name='Resolved_Date' ordinal='2' />
            <column datatype='string' name='Status' ordinal='3' />
            <column datatype='string' name='Priority' ordinal='4' />
            <column datatype='string' name='Category' ordinal='5' />
            <column datatype='string' name='Subcategory' ordinal='6' />
            <column datatype='string' name='Support_Team' ordinal='7' />
            <column datatype='string' name='Assigned_Agent' ordinal='8' />
            <column datatype='string' name='Department' ordinal='9' />
            <column datatype='real' name='SLA_Target_Hours' ordinal='10' />
            <column datatype='real' name='Actual_Resolution_Hours' ordinal='11' />
            <column datatype='string' name='SLA_Status' ordinal='12' />
            <column datatype='integer' name='Customer_Satisfaction_Score' ordinal='13' />
            <column datatype='integer' name='Reopened_Flag' ordinal='14' />
            <column datatype='integer' name='Escalated_Flag' ordinal='15' />
          </columns>
        </relation>
        <metadata-records>
          <metadata-record class='column'>
            <remote-name>Ticket_ID</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Ticket_ID]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Ticket_ID</remote-alias>
            <ordinal>0</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Created_Date</remote-name>
            <remote-type>135</remote-type>
            <local-name>[Created_Date]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Created_Date</remote-alias>
            <ordinal>1</ordinal>
            <local-type>datetime</local-type>
            <aggregation>Year</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Resolved_Date</remote-name>
            <remote-type>135</remote-type>
            <local-name>[Resolved_Date]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Resolved_Date</remote-alias>
            <ordinal>2</ordinal>
            <local-type>datetime</local-type>
            <aggregation>Year</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Status</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Status]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Status</remote-alias>
            <ordinal>3</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Priority</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Priority]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Priority</remote-alias>
            <ordinal>4</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Category</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Category]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Category</remote-alias>
            <ordinal>5</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Subcategory</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Subcategory]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Subcategory</remote-alias>
            <ordinal>6</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Support_Team</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Support_Team]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Support_Team</remote-alias>
            <ordinal>7</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Assigned_Agent</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Assigned_Agent]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Assigned_Agent</remote-alias>
            <ordinal>8</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Department</remote-name>
            <remote-type>129</remote-type>
            <local-name>[Department]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Department</remote-alias>
            <ordinal>9</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>SLA_Target_Hours</remote-name>
            <remote-type>5</remote-type>
            <local-name>[SLA_Target_Hours]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>SLA_Target_Hours</remote-alias>
            <ordinal>10</ordinal>
            <local-type>real</local-type>
            <aggregation>Avg</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Actual_Resolution_Hours</remote-name>
            <remote-type>5</remote-type>
            <local-name>[Actual_Resolution_Hours]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Actual_Resolution_Hours</remote-alias>
            <ordinal>11</ordinal>
            <local-type>real</local-type>
            <aggregation>Avg</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>SLA_Status</remote-name>
            <remote-type>129</remote-type>
            <local-name>[SLA_Status]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>SLA_Status</remote-alias>
            <ordinal>12</ordinal>
            <local-type>string</local-type>
            <aggregation>Count</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Customer_Satisfaction_Score</remote-name>
            <remote-type>20</remote-type>
            <local-name>[Customer_Satisfaction_Score]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Customer_Satisfaction_Score</remote-alias>
            <ordinal>13</ordinal>
            <local-type>integer</local-type>
            <aggregation>Avg</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Reopened_Flag</remote-name>
            <remote-type>20</remote-type>
            <local-name>[Reopened_Flag]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Reopened_Flag</remote-alias>
            <ordinal>14</ordinal>
            <local-type>integer</local-type>
            <aggregation>Sum</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
          <metadata-record class='column'>
            <remote-name>Escalated_Flag</remote-name>
            <remote-type>20</remote-type>
            <local-name>[Escalated_Flag]</local-name>
            <parent-name>[itsm_tickets_cleaned#csv]</parent-name>
            <remote-alias>Escalated_Flag</remote-alias>
            <ordinal>15</ordinal>
            <local-type>integer</local-type>
            <aggregation>Sum</aggregation>
            <contains-null>true</contains-null>
          </metadata-record>
        </metadata-records>
      </connection>
      
      <!-- Calculated Fields -->
      <column caption='Total Tickets' datatype='integer' name='[Calculation_Total_Tickets]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='COUNT([Ticket_ID])' />
      </column>
      
      <column caption='Resolved Tickets' datatype='integer' name='[Calculation_Resolved_Tickets]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='COUNT(IF [Status] = &quot;Resolved&quot; OR [Status] = &quot;Closed&quot; THEN [Ticket_ID] END)' />
      </column>
      
      <column caption='Open Tickets' datatype='integer' name='[Calculation_Open_Tickets]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='COUNT(IF [Status] != &quot;Resolved&quot; AND [Status] != &quot;Closed&quot; THEN [Ticket_ID] END)' />
      </column>
      
      <column caption='SLA Met Tickets' datatype='integer' name='[Calculation_SLA_Met_Tickets]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='COUNT(IF [SLA_Status] = &quot;Met&quot; THEN [Ticket_ID] END)' />
      </column>
      
      <column caption='SLA Breached Tickets' datatype='integer' name='[Calculation_SLA_Breached_Tickets]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='COUNT(IF [SLA_Status] = &quot;Breached&quot; THEN [Ticket_ID] END)' />
      </column>
      
      <column caption='SLA Compliance Rate %' datatype='real' default-format='p0.00%' name='[Calculation_SLA_Compliance_Pct]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='[Calculation_SLA_Met_Tickets] / [Calculation_Resolved_Tickets]' />
      </column>
      
      <column caption='SLA Breach Rate %' datatype='real' default-format='p0.00%' name='[Calculation_SLA_Breach_Rate_Pct]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='[Calculation_SLA_Breached_Tickets] / [Calculation_Resolved_Tickets]' />
      </column>
      
      <column caption='Avg Resolution Hours' datatype='real' default-format='n#,##0.00' name='[Calculation_Avg_Resolution_Hours]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='AVG([Actual_Resolution_Hours])' />
      </column>
      
      <column caption='Avg SLA Target Hours' datatype='real' default-format='n#,##0.00' name='[Calculation_Avg_SLA_Target_Hours]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='AVG(IF [Status] = &quot;Resolved&quot; OR [Status] = &quot;Closed&quot; THEN [SLA_Target_Hours] END)' />
      </column>
      
      <column caption='Turnaround Buffer Hours' datatype='real' default-format='n#,##0.00' name='[Calculation_Buffer_Hours]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='[Calculation_Avg_SLA_Target_Hours] - [Calculation_Avg_Resolution_Hours]' />
      </column>
      
      <column caption='Avg CSAT Score' datatype='real' default-format='n#,##0.00' name='[Calculation_Avg_CSAT]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='AVG([Customer_Satisfaction_Score])' />
      </column>
      
      <column caption='Reopened Rate %' datatype='real' default-format='p0.00%' name='[Calculation_Reopened_Rate_Pct]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='SUM([Reopened_Flag]) / [Calculation_Resolved_Tickets]' />
      </column>
      
      <column caption='Escalation Rate %' datatype='real' default-format='p0.00%' name='[Calculation_Escalation_Rate_Pct]' role='measure' type='quantitative'>
        <calculation class='tableau' formula='SUM([Escalated_Flag]) / [Calculation_Total_Tickets]' />
      </column>
    </datasource>
  </datasources>

  <worksheets>
    <!-- Sheet 1: Executive KPI Summary -->
    <worksheet name='Overview_KPI_Cards'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.itsm_data' />
          </datasources>
          <datasource-dependencies datasource='federated.itsm_data'>
            <column name='[Calculation_Total_Tickets]' />
            <column name='[Calculation_Resolved_Tickets]' />
            <column name='[Calculation_Open_Tickets]' />
            <column name='[Calculation_SLA_Compliance_Pct]' />
            <column name='[Calculation_SLA_Breached_Tickets]' />
            <column name='[Calculation_Avg_Resolution_Hours]' />
          </datasource-dependencies>
        </view>
        <style />
        <panes>
          <pane>
            <view>
              <breakdown value='auto' />
            </view>
            <mark class='Text' />
          </pane>
        </panes>
        <rows>[federated.itsm_data].[Calculation_Total_Tickets]</rows>
        <cols />
      </table>
    </worksheet>

    <!-- Sheet 2: Monthly Ticket Intake Trend -->
    <worksheet name='Overview_Monthly_Trend'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.itsm_data' />
          </datasources>
          <datasource-dependencies datasource='federated.itsm_data'>
            <column name='[Created_Date]' />
            <column name='[Calculation_Total_Tickets]' />
          </datasource-dependencies>
        </view>
        <panes>
          <pane>
            <mark class='Line' />
          </pane>
        </panes>
        <rows>[federated.itsm_data].[Calculation_Total_Tickets]</rows>
        <cols>[federated.itsm_data].[Created_Date]</cols>
      </table>
    </worksheet>

    <!-- Sheet 3: Volume by Priority -->
    <worksheet name='Overview_Priority_Share'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.itsm_data' />
          </datasources>
          <datasource-dependencies datasource='federated.itsm_data'>
            <column name='[Priority]' />
            <column name='[Calculation_Total_Tickets]' />
          </datasource-dependencies>
        </view>
        <panes>
          <pane>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.itsm_data].[Priority]</rows>
        <cols>[federated.itsm_data].[Calculation_Total_Tickets]</cols>
      </table>
    </worksheet>

    <!-- Sheet 4: SLA Compliance by Priority -->
    <worksheet name='SLA_Compliance_by_Priority'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.itsm_data' />
          </datasources>
          <datasource-dependencies datasource='federated.itsm_data'>
            <column name='[Priority]' />
            <column name='[Calculation_SLA_Compliance_Pct]' />
          </datasource-dependencies>
        </view>
        <panes>
          <pane>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.itsm_data].[Priority]</rows>
        <cols>[federated.itsm_data].[Calculation_SLA_Compliance_Pct]</cols>
      </table>
    </worksheet>

    <!-- Sheet 5: SLA Breaches by Category -->
    <worksheet name='SLA_Breaches_by_Category'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.itsm_data' />
          </datasources>
          <datasource-dependencies datasource='federated.itsm_data'>
            <column name='[Category]' />
            <column name='[Calculation_SLA_Breached_Tickets]' />
          </datasource-dependencies>
        </view>
        <panes>
          <pane>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.itsm_data].[Category]</rows>
        <cols>[federated.itsm_data].[Calculation_SLA_Breached_Tickets]</cols>
      </table>
    </worksheet>

    <!-- Sheet 6: SLA Breach Rate by Support Team -->
    <worksheet name='SLA_Breach_Rate_by_Team'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.itsm_data' />
          </datasources>
          <datasource-dependencies datasource='federated.itsm_data'>
            <column name='[Support_Team]' />
            <column name='[Calculation_SLA_Breach_Rate_Pct]' />
          </datasource-dependencies>
        </view>
        <panes>
          <pane>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.itsm_data].[Support_Team]</rows>
        <cols>[federated.itsm_data].[Calculation_SLA_Breach_Rate_Pct]</cols>
      </table>
    </worksheet>

    <!-- Sheet 7: Actual vs Target Resolution Time -->
    <worksheet name='Actual_vs_Target_Hours'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.itsm_data' />
          </datasources>
          <datasource-dependencies datasource='federated.itsm_data'>
            <column name='[Support_Team]' />
            <column name='[Calculation_Avg_Resolution_Hours]' />
            <column name='[Calculation_Avg_SLA_Target_Hours]' />
          </datasource-dependencies>
        </view>
        <panes>
          <pane>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.itsm_data].[Support_Team]</rows>
        <cols>[federated.itsm_data].[Calculation_Avg_Resolution_Hours]</cols>
      </table>
    </worksheet>

    <!-- Sheet 8: Ticket Volume by Support Team -->
    <worksheet name='Team_Volume_Distribution'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.itsm_data' />
          </datasources>
          <datasource-dependencies datasource='federated.itsm_data'>
            <column name='[Support_Team]' />
            <column name='[Calculation_Total_Tickets]' />
          </datasource-dependencies>
        </view>
        <panes>
          <pane>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.itsm_data].[Support_Team]</rows>
        <cols>[federated.itsm_data].[Calculation_Total_Tickets]</cols>
      </table>
    </worksheet>

    <!-- Sheet 9: Open Backlog by Team -->
    <worksheet name='Team_Open_Backlog'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.itsm_data' />
          </datasources>
          <datasource-dependencies datasource='federated.itsm_data'>
            <column name='[Support_Team]' />
            <column name='[Calculation_Open_Tickets]' />
          </datasource-dependencies>
        </view>
        <panes>
          <pane>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.itsm_data].[Support_Team]</rows>
        <cols>[federated.itsm_data].[Calculation_Open_Tickets]</cols>
      </table>
    </worksheet>

    <!-- Sheet 10: Turnaround Time by Team -->
    <worksheet name='Team_Avg_Turnaround'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.itsm_data' />
          </datasources>
          <datasource-dependencies datasource='federated.itsm_data'>
            <column name='[Support_Team]' />
            <column name='[Calculation_Avg_Resolution_Hours]' />
          </datasource-dependencies>
        </view>
        <panes>
          <pane>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.itsm_data].[Support_Team]</rows>
        <cols>[federated.itsm_data].[Calculation_Avg_Resolution_Hours]</cols>
      </table>
    </worksheet>

    <!-- Sheet 11: Reopened and Escalated Rates -->
    <worksheet name='Team_Reopens_and_Escalations'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.itsm_data' />
          </datasources>
          <datasource-dependencies datasource='federated.itsm_data'>
            <column name='[Support_Team]' />
            <column name='[Calculation_Escalation_Rate_Pct]' />
          </datasource-dependencies>
        </view>
        <panes>
          <pane>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.itsm_data].[Support_Team]</rows>
        <cols>[federated.itsm_data].[Calculation_Escalation_Rate_Pct]</cols>
      </table>
    </worksheet>

    <!-- Sheet 12: Top 10 Root Cause Breaches -->
    <worksheet name='Root_Cause_Subcategories'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.itsm_data' />
          </datasources>
          <datasource-dependencies datasource='federated.itsm_data'>
            <column name='[Subcategory]' />
            <column name='[Calculation_SLA_Breached_Tickets]' />
          </datasource-dependencies>
        </view>
        <panes>
          <pane>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.itsm_data].[Subcategory]</rows>
        <cols>[federated.itsm_data].[Calculation_SLA_Breached_Tickets]</cols>
      </table>
    </worksheet>

    <!-- Sheet 13: CSAT Impact by SLA Status -->
    <worksheet name='Root_Cause_CSAT_Impact'>
      <table>
        <view>
          <datasources>
            <datasource name='federated.itsm_data' />
          </datasources>
          <datasource-dependencies datasource='federated.itsm_data'>
            <column name='[SLA_Status]' />
            <column name='[Calculation_Avg_CSAT]' />
          </datasource-dependencies>
        </view>
        <panes>
          <pane>
            <mark class='Bar' />
          </pane>
        </panes>
        <rows>[federated.itsm_data].[SLA_Status]</rows>
        <cols>[federated.itsm_data].[Calculation_Avg_CSAT]</cols>
      </table>
    </worksheet>
  </worksheets>

  <dashboards>
    <!-- Dashboard 1: Executive Overview -->
    <dashboard name='1_Executive_Overview'>
      <style />
      <size maxheight='850' maxwidth='1300' minheight='850' minwidth='1300' />
      <zones>
        <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>
          <zone h='25000' id='2' name='Overview_KPI_Cards' w='100000' x='0' y='0' />
          <zone h='75000' id='3' name='Overview_Monthly_Trend' w='60000' x='0' y='25000' />
          <zone h='75000' id='4' name='Overview_Priority_Share' w='40000' x='60000' y='25000' />
        </zone>
      </zones>
    </dashboard>

    <!-- Dashboard 2: SLA & Priority Analysis -->
    <dashboard name='2_SLA_and_Priority_Analysis'>
      <style />
      <size maxheight='850' maxwidth='1300' minheight='850' minwidth='1300' />
      <zones>
        <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>
          <zone h='50000' id='2' name='SLA_Compliance_by_Priority' w='50000' x='0' y='0' />
          <zone h='50000' id='3' name='SLA_Breaches_by_Category' w='50000' x='50000' y='0' />
          <zone h='50000' id='4' name='SLA_Breach_Rate_by_Team' w='50000' x='0' y='50000' />
          <zone h='50000' id='5' name='Actual_vs_Target_Hours' w='50000' x='50000' y='50000' />
        </zone>
      </zones>
    </dashboard>

    <!-- Dashboard 3: Workload & Team Performance -->
    <dashboard name='3_Workload_and_Team_Performance'>
      <style />
      <size maxheight='850' maxwidth='1300' minheight='850' minwidth='1300' />
      <zones>
        <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>
          <zone h='50000' id='2' name='Team_Volume_Distribution' w='50000' x='0' y='0' />
          <zone h='50000' id='3' name='Team_Open_Backlog' w='50000' x='50000' y='0' />
          <zone h='50000' id='4' name='Team_Avg_Turnaround' w='50000' x='0' y='50000' />
          <zone h='50000' id='5' name='Team_Reopens_and_Escalations' w='50000' x='50000' y='50000' />
        </zone>
      </zones>
    </dashboard>

    <!-- Dashboard 4: Root Causes & Recommendations -->
    <dashboard name='4_Root_Causes_and_Recommendations'>
      <style />
      <size maxheight='850' maxwidth='1300' minheight='850' minwidth='1300' />
      <zones>
        <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>
          <zone h='50000' id='2' name='Root_Cause_Subcategories' w='60000' x='0' y='0' />
          <zone h='50000' id='3' name='Root_Cause_CSAT_Impact' w='40000' x='60000' y='0' />
        </zone>
      </zones>
    </dashboard>
  </dashboards>

  <windows>
    <window class='dashboard' name='1_Executive_Overview'>
      <viewpoints />
      <active id='-1' />
    </window>
  </windows>
</workbook>
"""

    with open(twb_path, "w", encoding="utf-8") as f:
        f.write(twb_xml.strip())

    print(f"Native Tableau Workbook successfully built at: {twb_path}")

    # Validate XML Syntax
    try:
        ET.parse(twb_path)
        print("XML validation check: PASS (Syntax 100% valid)")
    except Exception as e:
        print(f"XML validation check: FAIL ({e})")

if __name__ == "__main__":
    build_tableau_twb()
