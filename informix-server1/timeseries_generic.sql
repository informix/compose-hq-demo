database sysadmin;

execute function admin ('modify chunk extendable', 1);
execute function admin('STORAGEPOOL ADD', '$BASEDIR/data/spaces', 0,0,'64MB',1);

execute function admin('create dbspace', 'twsdbs', '$BASEDIR/data/spaces/dbs1', '200M', '0', '8');
execute function admin('create sbspace', 'twssbspace', '$BASEDIR/data/spaces/twssbspace', '20M', '0');

execute function admin('onmode', 'wf', 'SBSPACENAME=twssbspace');
execute function admin('onmode', 'wm', 'SBSPACENAME=twssbspace');


create database tsdb with log;

-- Needed to avoid autoregistration
execute function sysbldprepare('TimeSeries*', 'create');

create procedure tscreatevti(vti_tabname lvarchar, tabname lvarchar, calendar lvarchar, origin datetime year to fraction(5), type lvarchar)

define v_sql lvarchar;

let v_sql="execute procedure tscreatevirtualtab('" || vti_tabname || 
          "', '" ||tabname || "', 'calendar(" || calendar || 
          "), origin(" || origin || "), irregular')"  ;

execute immediate v_sql; 
end procedure;

create row type tstab_data_t
(
   tstamp datetime year to fraction(5),
   json_data bson
);


create table tstab
(
   id varchar(255) not null primary key,
   properties bson,
   data timeseries(tstab_data_t)
);

-- Use of wrapper.  Can specify current - (1 day), etc.
--execute procedure tscreatevti('tstab_v' , 'tstab', 'ts_1min',current, 'irregular'); 


execute procedure tscreatevirtualtab('tstab_v' , 'tstab', 'calendar(ts_1min), origin(%Y-%m-%d 00:00:00.00000),irregular'); 
